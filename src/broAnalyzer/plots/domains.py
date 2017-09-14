from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class DomainsPlot(Plot):

    def __init__(self):
        super(DomainsPlot, self).__init__('Domains', 'DomainsByDay.csv', 'domains')
        self.__output_file_name = "DomainsByDay.png"

    def add_args(self, parser):
        parser.add_argument('-dd', '--domains', action='store_true',
                            help='Plot domain names extracted from Bro log files')

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

        fig = plotDataFrame(df, "Domains per Day")
        formatXAxisDate(fig)

        plt.savefig(join(output_folder, self.__output_file_name))
