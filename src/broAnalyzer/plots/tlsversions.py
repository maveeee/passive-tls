from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class TlsVersionsPlot(Plot):

    def __init__(self):
        super(TlsVersionsPlot, self).__init__('TLS Versions', 'TLSVersionsByDay.csv', 'tlsVersions')
        self.__output_file_name = "TLSVersionsByDay.png"

    def add_args(self, parser):
        parser.add_argument('-t', '--tlsVersions', action='store_true',
                            help='Plot TLS version information extracted from Bro log files')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(
            input_file, sep='\x09', index_col=[0, 1], parse_dates=[0]) \
            .unstack(level=1).fillna(0)
        df.columns = df.columns.droplevel()

        df.columns.name = None
        df.index.name = None

        fig = plotDataFrame(df, "Number of TLS Connections per Day")
        formatXAxisDate(fig)

        plt.savefig(join(output_folder, self.__output_file_name))
