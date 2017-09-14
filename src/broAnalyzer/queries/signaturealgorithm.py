from util.query import CertificateQuery
from util.functions import defaultReduceDataFrames

class SignatureAlgorithmQuery(CertificateQuery):

    __name = 'Signature Algorithm'
    __parameter_name = 'signatureAlgorithm'
    __file_name = 'SignatureAlgorithmByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-si', '--signatureAlgorithm', action='store_true',
                            help='Extract signature algorithm information from certificates')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df[['Day', 'SignatureAlgorithm']].groupby(['Day', 'SignatureAlgorithm']).size() \
                .rename('Count').reset_index().set_index(['Day', 'SignatureAlgorithm'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
