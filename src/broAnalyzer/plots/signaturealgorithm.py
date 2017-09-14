from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class SignatureAlgorithmPlot(Plot):

    def __init__(self):
        super(SignatureAlgorithmPlot, self).__init__('Signature Algorithm', 'SignatureAlgorithmByDay.csv', 'signatureAlgorithm')
        self.__output_file_name = "SignatureAlgorithmByDay.png"

    def add_args(self, parser):
        parser.add_argument('-si', '--signatureAlgorithm', action='store_true',
                            help='Plot certificate signature algorithm information')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(
            input_file, sep='\x09', index_col=[0, 1], parse_dates=[0]) \
            .unstack(level=1).fillna(0)
        df.columns = df.columns.droplevel()

        df.columns.name = None
        df.index.name = None

        df = df[df.sum().sort_values(ascending=False).head(5).index.values]

        fig = plotDataFrame(df, "Most used Signature Algorithms")
        fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        formatXAxisDate(fig)

        plt.tight_layout()

        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
