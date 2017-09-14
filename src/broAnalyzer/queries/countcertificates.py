from util.query import CertificateQuery
from util.functions import defaultReduceDataFrames

class CountCertificatesQuery(CertificateQuery):

    __name = 'Count Certificates'
    __parameter_name = 'countCerts'
    __file_name = 'NumberOfCertificatesByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-cc', '--countCerts', action='store_true',
                            help='Count the number of certificates seen each day')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df.groupby(['Day']).size().rename('Count').reset_index().set_index(['Day'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
