from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class PortsPlot(Plot):

    def __init__(self):
        super(PortsPlot, self).__init__('Ports', 'PortsByDay.csv', 'ports')
        self.__output_file_name1 = "PortsByDay.png"
        self.__output_file_name2 = "PortsByDayWithout443.png"

    def add_args(self, parser):
        parser.add_argument('-p', '--ports', action='store_true',
                            help='Plot port information extracted from Bro log files')


    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(
            input_file, sep='\x09', index_col=[0, 1], parse_dates=[0]) \
            .unstack(level=1).fillna(0)

        df.columns = df.columns.droplevel()

        df.columns.name = None
        df.index.name = None

        topXPorts = df.sum().sort_values(ascending=False).head(6).index.values

        topPorts = df[topXPorts[:5]]
        topPortsWithout443 = df[[p for p in topXPorts if p != 443][:5]]

        fig = plotDataFrame(topPorts, "Ports per Day")
        formatXAxisDate(fig)

        plt.savefig(join(output_folder, self.__output_file_name1))

        fig = plotDataFrame(topPortsWithout443, "Ports per Day (without 443)")
        formatXAxisDate(fig)

        plt.savefig(join(output_folder, self.__output_file_name2))
