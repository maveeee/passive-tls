from os.path import isfile
import pandas as pd

def defaultReduceDataFrames(dfs):
    return reduce(lambda x, y: x.add(y, fill_value=0), dfs)

def concatDataFrames(dfs):
    df = pd.concat(dfs)
    return df

def parseSpecificDomains(fileName):
    if isfile(fileName):
        return pd.read_csv(fileName, sep='\x09', header=None, names=['Domain'], dtype={'Domain': str})['Domain'].values.tolist()
    else:
        return []

#   see https://github.com/pyca/pyopenssl/issues/386

def formatX509Name(x509Name):
    return ', '.join(['{}={}'.format(x, y) for x, y in x509Name.get_components()]).decode("iso8859")
