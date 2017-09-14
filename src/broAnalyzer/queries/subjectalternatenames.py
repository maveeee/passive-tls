from util.query import CertificateQuery
from util.functions import concatDataFrames
from util import extensionParser

class SubjectAlternateNamesQuery(CertificateQuery):

    __name = 'Subject Alternate Names'
    __parameter_name = 'subjectAltNames'
    __file_name = 'SubjectAlternateNames.csv'

    def get_name(self):
        return self.__name

    def get_file_name(self):
        return self.__file_name

    def get_arg_name(self):
        return self.__parameter_name

    def add_args(self, parser):
        parser.add_argument('-san', '--subjectAltNames', action='store_true',
                            help='Extract subject alternate names from certificates')


    def parse_args(self, args):
        pass

    def apply(self, df):
        df['SubjectAltNames'] = df.apply(extractSANListFromRow, axis=1, raw=True)
        return df[['Day', 'FileName', 'SubjectAltNames']].dropna().set_index(['Day'])

    def reduce(self, dfs):
        return concatDataFrames(dfs)

def extractSANListFromRow(row):
    if 'subjectAltName' in row[2]:
        i = row[2].index('subjectAltName')
        sanList = extensionParser.decodeAsn1Extension('subjectAltName',
                                                      row[0].get_extension(i).get_data())
        return str(sanList)
