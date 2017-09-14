from util.query import LogEntryQuery
from util.functions import defaultReduceDataFrames

class DomainsQuery(LogEntryQuery):

    __name = 'Domains'
    __parameter_name = 'domains'
    __file_name = 'DomainsByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-dd', '--domains', action='store_true',
                            help='Extract domain names (2 levels) from Bro log files')

    def parse_args(self, args):
        pass

    def apply(self, df):
        return df.groupby(['Day', 'Domain'], sort=False, as_index=False).size() \
            .rename('Count').reset_index().set_index(['Day', 'Domain'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)
