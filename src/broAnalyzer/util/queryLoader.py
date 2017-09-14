import pkgutil
from .query import Query, CertificateQuery, LogEntryQuery

class QueryLoader(object):
    """ Used to load query objects from given module """

    def __init__(self, path):
        self.path = path
        self.__modules = []
        self.__queries = []

    def get_queries(self):
        if not self.__modules:
            self.__init_queries()
        return self.__queries

    def __init_queries(self):
        self.__load_modules()
        self.__queries = [cls for cls in self.__get_all_subclasses(Query) if cls != CertificateQuery and cls != LogEntryQuery]

    def __load_modules(self):
        for importer, package_name, _ in pkgutil.iter_modules([self.path]):
            self.__modules.append(importer.find_module(package_name).load_module(package_name))

    def __get_all_subclasses(self, clazz):
        subclasses = set()
        remainingClasses = [clazz]
        while remainingClasses:
            parent = remainingClasses.pop()
            for child in [c for c in parent.__subclasses__() if c not in subclasses]:
                subclasses.add(child)
                remainingClasses.append(child)
        return list(subclasses)
