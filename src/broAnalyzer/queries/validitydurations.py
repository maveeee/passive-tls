import logging
from datetime import datetime
from util.query import CertificateQuery
from util.functions import defaultReduceDataFrames

log = logging.getLogger(__name__)

class ValidityDurationQuery(CertificateQuery):

    __name = 'Average Validity Duration'
    __parameter_name = 'validityDuration'
    __file_name = 'AverageValidityDurationByDay.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-vd', '--validityDuration', action='store_true',
                            help='Extracts the average certificate validtiy duration')

    def parse_args(self, args):
        pass

    def apply(self, df):
        df['ValidityDuration'] = df.apply((lambda row: calcValidityDuration(row['NotAfter'], row['NotBefore'])), axis=1)
        return df.groupby(['Day'])['ValidityDuration'].agg(['mean', 'median', 'max', 'min']).reset_index().set_index(['Day'])

    def reduce(self, dfs):
        return defaultReduceDataFrames(dfs)

def calcValidityDuration(t1, t2):
    try:
        duration = (datetime.strptime(t1, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(t2, "%Y-%m-%dT%H:%M:%S")).days

        if duration <= 0:
            log.warning('Negative certificate validity duration: %i, using absolute value. (t1: %s, t2: %s', duration, t1, t2)
            return abs(duration)
        return duration
    except:
        log.error("Calculating validity duration! t1: %s, t2: %s", t1, t2)
        return 0
