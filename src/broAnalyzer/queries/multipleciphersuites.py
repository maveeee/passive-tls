from util.query import LogEntryQuery
import pandas as pd

class MutipleCipherSuitesQuery(LogEntryQuery):

    __name = 'Multiple Cipher Suites'
    __parameter_name = 'mutipleCipherSuites'
    __file_name = 'ServersWithMultipleCiphersByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-mc', '--mutipleCipherSuites', action='store_true',
                            help='extract servers which use multiple cipher suites')

    def parse_args(self, args):
        pass

    def apply(self, df):
        x = df.groupby(['Day', 'Server Name'], sort=False, as_index=False)['Cipher'] \
            .apply(lambda x: len(x.dropna().unique()))[lambda x: x > 2] \
            .rename('Cipher').reset_index().set_index(['Day', 'Server Name'])
        y = df[['Day', 'Server Name', 'Cipher']].dropna().set_index(['Day', 'Server Name'])
        return y[y.index.isin(x.index)].reset_index() \
            .drop_duplicates().set_index(['Day', 'Server Name'])

    def reduce(self, dfs):
        df = pd.concat(dfs)
        return df.reset_index().drop_duplicates().set_index(['Day', 'Server Name'])

