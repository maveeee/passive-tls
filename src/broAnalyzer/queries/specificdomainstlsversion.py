from os.path import join
from util.query import LogEntryQuery
from util.functions import concatDataFrames, parseSpecificDomains

class SpeficiDomainsTlsVersionsQuery(LogEntryQuery):

    __name = 'Specific Domain TLS Versions'
    __parameter_name = 'specificDomainsTLSVersions'
    __file_name = 'SpecificDomainTLSVersionsByDay.csv'

    def __init__(self):
        self.__domains = []

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-sdv', '--specificDomainsTLSVersions', action='store_true',
                            help='extract TLS version information for the domains in the file supplied via parameter -sd ')
        parser.add_argument('-sd', '--specificDomains', action='store', default='domains.csv',
                            help='Name of the file (within data dir) containing the domains used for specific domain queries')

    def parse_args(self, args):
        domainsFileName = join(args.dataDir, args.specificDomains)
        self.__domains = parseSpecificDomains(domainsFileName)

    def apply(self, df):
        return df[df['Domain'].isin(self.__domains)][['Day', 'Timestamp', 'Domain', 'Version']] \
            .dropna().set_index(['Day', 'Domain'])

    def reduce(self, dfs):
        return concatDataFrames(dfs)
