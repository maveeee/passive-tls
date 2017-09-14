from util.query import LogEntryQuery
from util.functions import defaultReduceDataFrames

class CipherSuitesQuery(LogEntryQuery):

    __name = 'Cipher Suites'
    __parameter_name = 'cipherSuites'
    __file_name = 'CipherSuitesByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-c', '--cipherSuites', action='store_true',
                            help='Extract cipher suite information from Bro log files')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df.groupby(['Day', 'Cipher'], sort=False, as_index=False).size() \
            .rename('Count').reset_index().set_index(['Day', 'Cipher'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
