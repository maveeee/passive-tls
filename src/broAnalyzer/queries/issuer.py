from util.query import CertificateQuery
from util.functions import defaultReduceDataFrames, formatX509Name

class IssuerQuery(CertificateQuery):

    __name = 'Issuer'
    __parameter_name = 'issuer'
    __file_name = 'IssuerByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-i', '--issuer', action='store_true',
                            help='Extract issuer information from certificates')

    def parse_args(self, args):
        pass

    def apply(self, df):
        df['Issuer'] = df['Issuer'].apply(formatX509Name)
        return df[['Day', 'Issuer']].groupby(['Day', 'Issuer']).size() \
                    .rename('Count').reset_index().set_index(['Day', 'Issuer'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
