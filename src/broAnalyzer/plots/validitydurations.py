from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class ValidityDurationPlot(Plot):

    def __init__(self):
        super(ValidityDurationPlot, self).__init__('Average Validity Duration', 'AverageValidityDurationByDay.csv', 'validityDuration')
        self.__output_file_name = "AverageValidityDurationByDay.png"

    def add_args(self, parser):
        parser.add_argument('-vd', '--validityDuration', action='store_true',
                            help='Plots the average certificate validtiy duration')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(input_file, sep='\x09', index_col=[0], parse_dates=[0])

        df.columns.name = None
        df.index.name = None

        fig = plotDataFrame(df, "Average Certificate Validity Duration")
        formatXAxisDate(fig)

        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
