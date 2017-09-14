from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, plotDataFrame, formatXAxisDate

class SubjectAlternateNamesPlot(Plot):

    def __init__(self):
        super(SubjectAlternateNamesPlot, self).__init__('Subject Alternate Names', 'SubjectAlternateNames.csv', 'subjectAltNames')
        self.__output_file_name = "SubjectAlternateNames.png"

    def add_args(self, parser):
        parser.add_argument('-san', '--subjectAltNames', action='store_true',
                            help='Plot subject alternate names from certificates')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(input_file,
                         sep='\x09', usecols=[0, 1, 2], parse_dates=[0], converters={"SubjectAltNames": lambda x: x.strip("[]").split(", ")})

        df.dropna(inplace=True)
        df['SANLength'] = df['SubjectAltNames'].apply(lambda x:len(x) if isinstance(x, list) else None)

        df = df.groupby('Day')['SANLength'].agg(['mean', 'median', 'max', 'min'])

        df.columns.name = None
        df.index.name = None

        fig = plotDataFrame(df, "Length of Subject Alternate Name List")
        fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        formatXAxisDate(fig)

        plt.tight_layout()

        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
