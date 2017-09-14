import pkgutil
from .plot import Plot

class PlotLoader(object):
    """ Used to load plot objects from given module """

    def __init__(self, path):
        self.path = path
        self.__modules = []
        self.__plots = []

    def get_plots(self):
        if not self.__modules:
            self.__init_plots()
        return self.__plots

    def __init_plots(self):
        self.__load_modules()
        self.__plots = self.__get_all_subclasses(Plot)

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
