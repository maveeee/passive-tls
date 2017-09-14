from util.query import LogEntryQuery
from util.functions import defaultReduceDataFrames

class TlsVersionsQuery(LogEntryQuery):

    __name = 'TLS Versions'
    __parameter_name = 'tlsVersions'
    __file_name = 'TLSVersionsByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-t', '--tlsVersions', action='store_true',
                            help='Extract used TLS versions from Bro log files')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df.groupby(['Day', 'Version'], sort=False, as_index=False).size() \
            .rename('Count').reset_index().set_index(['Day', 'Version'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
