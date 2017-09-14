from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class CountCertificatesPlot(Plot):

    def __init__(self):
        super(CountCertificatesPlot, self).__init__('Count Certificates', 'NumberOfCertificatesByDay.csv', 'countCerts')
        self.__output_file_name = "NumberOfCertificatesByDay.png"

    def add_args(self, parser):
        parser.add_argument('-cc', '--countCerts', action='store_true',
                            help='Plot the number of certificates seen each day')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(
            input_file, sep='\x09', index_col=[0], parse_dates=[0])

        df.columns.name = None
        df.index.name = None

        fig = plotDataFrame(df, "Number of Certificates by Day")
        formatXAxisDate(fig)

        plt.tight_layout()
        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
