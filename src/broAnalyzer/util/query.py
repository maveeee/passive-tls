class Query(object):

    def get_name(self):
        raise NotImplementedError

    def get_file_name(self):
        raise NotImplementedError

    def get_arg_name(self):
        raise NotImplementedError

    def add_args(self, parser):
        raise NotImplementedError

    def parse_args(self, args):
        raise NotImplementedError

    def apply(self, df):
        raise NotImplementedError

    def reduce(self, dfs):
        raise NotImplementedError

class LogEntryQuery(Query):
    pass

class CertificateQuery(Query):
    pass
