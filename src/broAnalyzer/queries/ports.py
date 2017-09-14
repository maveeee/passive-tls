from util.query import LogEntryQuery
from util.functions import defaultReduceDataFrames

class PortsQuery(LogEntryQuery):

    __name = 'Ports'
    __parameter_name = 'ports'
    __file_name = 'PortsByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-p', '--ports', action='store_true',
                            help='Extract used ports from Bro log files')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df.groupby(['Day', 'Port'], sort=False, as_index=False).size() \
            .rename('Count').reset_index().set_index(['Day', 'Port'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
