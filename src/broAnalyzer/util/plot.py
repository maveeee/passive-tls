from os.path import join, isfile
import matplotlib.dates as mdates

class Plot(object):
    def __init__(self, name, input_file_name, arg_name):
        self.name = name
        self.input_file_name = input_file_name
        self.arg_name = arg_name

    def get_name(self):
        return self.name

    def get_input_file_name(self):
        return self.input_file_name

    def get_arg_name(self):
        return self.arg_name

    def parse_args(self, args):
        raise NotImplementedError

    def add_args(self, parser):
        raise NotImplementedError

    def plot(self, input_file, output_folder):
        raise NotImplementedError

    def verify_input_file(self, input_folder):
        fileName = join(input_folder, self.get_input_file_name())
        return isfile(fileName)

def formatXAxisDate(fig):
    fig.xaxis.set_minor_locator(mdates.DayLocator())
    fig.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    fig.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

def plotDataFrame(df, title):
    return df.plot(title=title, grid=True, style=['.'] * len(df.columns))
