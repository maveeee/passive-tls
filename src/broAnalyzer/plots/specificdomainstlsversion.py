from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
from util.plot import Plot, formatXAxisDate

class SpeficiDomainsTlsVersionsPlot(Plot):

    def __init__(self):
        super(SpeficiDomainsTlsVersionsPlot, self).__init__('Specific Domain TLS Versions', 'SpecificDomainTLSVersionsByDay.csv', 'specificDomainsCipher')
        self.__output_file_name = "SpecificDomainTLSVersionsByDay.png"

    def add_args(self, parser):
        parser.add_argument('-sdv', '--specificDomainsTLSVersions', action='store_true',
                            help='Plot TLS version information for specific domains')

    def parse_args(self, args):
        pass

    def plot(self, input_file, output_folder):
        df = pd.read_csv(input_file,
                         sep='\x09', usecols=[0, 1, 3], parse_dates=[0])

        domains = df['Domain'].unique().tolist()

        fig, axes = plt.subplots(nrows=len(domains))
        fig.suptitle('Top 3 TLS Versions per Day and Domain', fontsize=12)

        for i, domain in enumerate(domains):
            x = df[df['Domain'] == domain].drop('Domain', axis=1) \
                .groupby(['Day', 'Version']).size().unstack()
            x = x[x.sum().sort_values(ascending=False).head(3).index.values]

            x.columns.name = None
            x.index.name = None

            ax = x.plot(title=domain, grid=True, style=['.'] * len(x.columns), ax=axes[i])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            formatXAxisDate(ax)

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(join(output_folder, self.__output_file_name), bbox_inches='tight')
