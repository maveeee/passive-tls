from os import listdir, makedirs
from os.path import join, isdir, dirname, abspath, basename
import logging
import argparse
from util.queryLoader import QueryLoader
from util.query import LogEntryQuery, CertificateQuery
from util.parser import parseLogFiles, parseCertificates

log = logging.getLogger(__name__)


def import_queries():
    queryLoader = QueryLoader(join(dirname(__file__), 'queries'))
    return [q() for q in queryLoader.get_queries()]

def parse_arguments(queries):
    parser = argparse.ArgumentParser(description='Analyze Bro log files', conflict_handler='resolve')

    parser.add_argument('-d', '--dataDir', action='store', default='data',
                        help='directory which holds the Bro data (log files, certificates)')
    parser.add_argument('-o', '--outputDir', action='store', default='out',
                        help='directory to store the output files')
    parser.add_argument('-v', '--verbosity', action='store',
                        choices=[logging.getLevelName(level) for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]],
                        default=logging.getLevelName(logging.INFO), help='specify the degree of verbosity')

    parser.add_argument('-a', '--all', action='store_true',
                        help='apply all extraction functions')

    for q in queries:
        q.add_args(parser)

    args = parser.parse_args()

    if args.all:
        for q in queries:
            args.__dict__[q.get_arg_name()] = True

    # use only active queries
    queries = [q for q in queries if args.__dict__[q.get_arg_name()]]

    for q in queries:
        q.parse_args(args)

    args.parseLogEntries = \
        any([isinstance(q, LogEntryQuery) for q in queries])
    args.parseCertificates = \
        any([isinstance(q, CertificateQuery) for q in queries])

    if (not args.parseLogEntries) and (not args.parseCertificates):
        parser.error('Specify at least one parsing option!')
    else:
        return (args, queries)

def configureLogging(loglevel):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.getLevelName(loglevel))

def outputData(df, filename):
    df.to_csv(filename, sep='\t', encoding='utf-8')

def ensureFolder(path):
    path = abspath(path)
    if not isdir(path):
        log.debug('Folder ''%s'' does not exist! Creating folder.', path)
        makedirs(path)

def handleLogEntryQueries(queryData, queries, folder, args):
    if not args.parseLogEntries:
        return

    logFolder = abspath(join(folder, 'logs'))

    if isdir(logFolder):
        log.info('Parsing Bro log files from ''%s''.', logFolder)

        logEntries = parseLogFiles(logFolder)
        if logEntries is not None and not logEntries.empty:
            for q in queries:
                if isinstance(q, LogEntryQuery):
                    try:
                        log.debug('Executing query ''%s''.', type(q).__name__)
                        queryData[q].append(q.apply(logEntries.copy()))
                    except:
                        log.exception('Failed to execute query ''%s''!', type(q).__name__)
        else:
            log.warning('No log entries found in ''%s''!', logFolder)
    else:
        log.warning('Log folder ''%s'' does not exist!', logFolder)

def handleCertificateQueries(queryData, queries, folder, args):
    if not args.parseCertificates:
        return

    certFolder = join(folder, 'certificates')

    if isdir(certFolder):
        log.info('Parsing certificates from ''%s''.', certFolder)
        
        certificates = parseCertificates(certFolder, basename(folder))
        if certificates is not None and not certificates.empty:
            for q in queries:
                if isinstance(q, CertificateQuery):
                    try:
                        log.debug('Executing query ''%s''.', type(q).__name__)
                        queryData[q].append(q.apply(certificates.copy()))
                    except:
                        log.exception('Failed to execute query ''%s''!', type(q).__name__)
        else:
            log.warning('No certificates found in ''%s''!', certFolder)
    else:
        log.warning('Certificate folder ''%s'' does not exist!', certFolder)


def main():
    queries = import_queries()
    args, queries = parse_arguments(queries)
    configureLogging(args.verbosity)

    log.info('Begin of TLS analysis...')

    ensureFolder(args.outputDir)

    queryData = {}
    for q in queries:
        queryData[q] = []

    for folder in sorted([f for f in [join(args.dataDir, x) for x in listdir(args.dataDir)] if isdir(f)]):

        handleLogEntryQueries(queryData, queries, folder, args)
        handleCertificateQueries(queryData, queries, folder, args)

    for query, dfs in queryData.iteritems():
        if dfs:
            df = query.reduce(dfs)

        log.info('Writing file ''%s''.', query.get_file_name())
        outputData(df.sort_index(ascending=False), join(args.outputDir, query.get_file_name()))

    log.info('Finished TLS analysis')

if __name__ == "__main__":
    main()
