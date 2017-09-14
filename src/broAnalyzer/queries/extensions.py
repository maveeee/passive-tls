import pandas as pd
from util.query import CertificateQuery
from util.functions import concatDataFrames

class ExtensionsQuery(CertificateQuery):

    __name = 'Extensions'
    __parameter_name = 'extensions'
    __file_name = 'ExtensionsByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-x', '--extensions', action='store_true',
                            help='Extracts the certificate extensions')

    def parse_args(self, args):
        pass

    def apply(self, df):
        df = df[['Day', 'FileName', 'Extensions']]
        rows = []
        for row in df.itertuples(): # dataframe index is on tuple index 0
            for extension in row[3]:
                rows.append([row[1], row[2], extension])

        df = pd.DataFrame(rows, columns=['Day', 'FileName', 'Extension'])
        return df.set_index(['Day', 'FileName'])

    def reduce(self, dfs):
        return concatDataFrames(dfs)
