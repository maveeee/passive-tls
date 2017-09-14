from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class ExtensionsPlot(Plot):

    def __init__(self):
        super(ExtensionsPlot, self).__init__('Extensions', 'ExtensionsByDay.csv', 'extensions')
        self.__output_file_name = "ExtensionsByDay.png"

    def add_args(self, parser):
        parser.add_argument('-x', '--extensions', action='store_true',
                            help='Plot certificate extension information')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(input_file,
                         sep='\x09', usecols=[0, 1, 2], parse_dates=[0]) \
            .groupby(['Day', 'Extension']).size().rename('Count')

        top5Extensions = df.reset_index() \
            .groupby(['Extension']) \
            .sum() \
            .sort_values(by='Count', ascending=False) \
            .head(5).index.values
        df = df.unstack()[top5Extensions]

        df.columns.name = None
        df.index.name = None

        fig = plotDataFrame(df, "Most used Certificate Extensions")
        fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        formatXAxisDate(fig)

        plt.tight_layout()

        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
