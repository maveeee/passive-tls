from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class CipherSuitesPlot(Plot):

    def __init__(self):
        super(CipherSuitesPlot, self).__init__('Cipher Suites', 'CipherSuitesByDay.csv', 'cipherSuites')
        self.__output_file_name = "CipherSuitesByDay.png"

    def add_args(self, parser):
        parser.add_argument('-c', '--cipherSuites', action='store_true',
                            help='Plot cipher suite information extracted from Bro log files')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        raw = pd.read_csv(
                input_file, sep='\x09', index_col=[0, 1], parse_dates=[0])

        df = raw.unstack(level=1).fillna(0)

        df.columns = df.columns.droplevel()

        df.columns.name = None
        df.index.name = None

        cipherSuites = df[df.sum().sort_values(ascending=False).head(5).index.values]

        fig = plotDataFrame(cipherSuites, "Cipher Suites per Day")
        formatXAxisDate(fig)
        plt.savefig(join(output_folder, self.__output_file_name))
