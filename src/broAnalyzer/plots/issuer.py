from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class IssuerPlot(Plot):

    def __init__(self):
        super(IssuerPlot, self).__init__('Issuer', 'IssuerByDay.csv', 'issuer')
        self.__output_file_name = "IssuerByDay.png"

    def add_args(self, parser):
        parser.add_argument('-i', '--issuer', action='store_true',
                            help='Plot certificate issuer information')

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

        fig = plotDataFrame(df, "Top Issuer")
        fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
        formatXAxisDate(fig)

        plt.tight_layout()
        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
