import logging
import argparse
import matplotlib
import matplotlib.pyplot as plt
from os import makedirs
from os.path import join, isfile, isdir, dirname, abspath
from util.plotLoader import PlotLoader
from util.plot import Plot

log = logging.getLogger(__name__)

def import_plots():
    plotLoader = PlotLoader(join(dirname(__file__), 'plots'))
    return [q() for q in plotLoader.get_plots()]

def ensureFolder(path):
    path = abspath(path)
    if not isdir(path):
        log.debug('Folder ''%s'' does not exist! Creating folder.', path)
        makedirs(path)

def parse_arguments(plots):
    parser = argparse.ArgumentParser(description='Analyze Bro log files', conflict_handler='resolve')

    parser.add_argument('-d', '--dataDir', action='store', default='out',
                        help='directory which holds query data files')
    parser.add_argument('-o', '--outputDir', action='store', default='out',
                        help='directory to store the plots')
    parser.add_argument('-v', '--verbosity', action='store',
                        choices=[logging.getLevelName(level) for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]],
                        default=logging.getLevelName(logging.INFO), help='specify the degree of verbosity')

    parser.add_argument('-a', '--all', action='store_true',
                        help='apply all plots')

    for p in plots:
        p.add_args(parser)

    args = parser.parse_args()

    if args.all:
        for p in plots:
            args.__dict__[p.get_arg_name()] = True

    # use only active plots
    plots = [p for p in plots if args.__dict__[p.get_arg_name()]]

    for p in plots:
        p.parse_args(args)

    return (args, plots)

def configureLogging(loglevel):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.getLevelName(loglevel))

def main():
    plots = import_plots()
    args, plots = parse_arguments(plots)
    configureLogging(args.verbosity)

    ensureFolder(args.outputDir)

    plt.switch_backend('Agg')
    matplotlib.style.use('ggplot')

    for p in plots:
        log.info('Processing plot ''%s''.', type(p).__name__)
        input_file = join(args.dataDir, p.get_input_file_name())
        if not isfile(input_file):
            log.warning('Input file ''%s'' does not exist!', input_file)
            continue
        try:
            p.plot(input_file, args.outputDir)
        except:
            log.exception('Failed to process plot ''%s''!', type(p).__name__)


if __name__ == "__main__":
    main()
