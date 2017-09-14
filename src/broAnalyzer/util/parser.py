from os import listdir
from os.path import isfile, isdir, join, basename
from datetime import datetime
import re
import pandas as pd
import OpenSSL


def listFiles(path, extension):
    return [f for f in [join(path, x) for x in listdir(path)]
            if isfile(f) and f.endswith(extension)] if isdir(path) else []

def parseUnixEpoch(epoch_list):
    return [datetime.fromtimestamp(float(x)) for x in epoch_list]

def parseLogFiles(path):
    columnNames = ['Timestamp',
                   'Uid',
                   'SourceIP',
                   'SourcePort',
                   'IP',
                   'Port',
                   'Version',
                   'Cipher',
                   'Curve',
                   'Server Name',
                   'Resumed',
                   'Last Alert',
                   'Next Protocol',
                   'Established',
                   'Cert Chain Fuids',
                   'Client Cert Chain Fuids',
                   'Subject',
                   'Issuer',
                   'Client Subject',
                   'Client Issuer',
                   'Validation Status']
    useCols = [0, 4, 5, 6, 7, 8, 9, 14, 16, 17]

    fileNames = listFiles(path, '.log')
    dfs = [None] * len(fileNames)
    for i, fileName in enumerate(fileNames):
        dfs[i] = pd.read_csv(
            fileName,
            sep='\x09',
            na_values=['-', '(empty)'],
            comment='#',
            header=None,
            names=columnNames, usecols=useCols,
            parse_dates=['Timestamp'], date_parser=parseUnixEpoch,
            dtype={'IP': str, 'Port': int, 'Version': str, 'Cipher': str, 'Curve': str, 'Server Name': str, 'Cert Chain Fuids': str, 'Subject': str, 'Issuer': str,})

    if dfs and all([not (x is None) for x in dfs]):
        df = pd.concat(dfs)
        df['Cert Chain Fuids'] = df['Cert Chain Fuids'].map(lambda x: x.split(','), na_action='ignore')
        df['Day'] = df['Timestamp'].map(lambda ts: ts.date())
        df['Domain'] = df['Server Name'] \
            .str.extract(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', expand=False) \
            .fillna(df['Server Name'].str.rsplit('.', n=2) \
            .apply(lambda x: '.'.join(x[1:]) if isinstance(x, list) and len(x) > 2 else ('.'.join(x) if isinstance(x, list) else x)))
        return df
    else:
        return None

def parseCertificates(path, day):
    certificates = loadCertificates(path)

    columnDict = {
        'FileName': [],
        'Issuer' : [],
        'SignatureAlgorithm' : [],
        'NotBefore' : [],
        'NotAfter' : [],
        'Version' : [],
        'SerialNumber' : [],
        'Subject' : [],
        'Extensions' : [],
        'CertObject' : []
        }

    for fileName, c in certificates.iteritems():
        columnDict['Day'] = day
        columnDict['FileName'].append(basename(fileName))
        columnDict['Issuer'].append(c.get_issuer())
        columnDict['SignatureAlgorithm'].append(c.get_signature_algorithm())
        columnDict['NotBefore'].append(parseAsn1DateString(c.get_notBefore()))
        columnDict['NotAfter'].append(parseAsn1DateString(c.get_notAfter()))
        columnDict['Version'].append(c.get_version())
        columnDict['SerialNumber'].append('{0:x}'.format(c.get_serial_number()))
        columnDict['Subject'].append(c.get_subject())

        columnDict['Extensions'].append(
            [c.get_extension(i).get_short_name() for i in range(c.get_extension_count())])

        columnDict['CertObject'].append(c)

    return pd.DataFrame(columnDict)

def loadCertificates(path):
    fileNames = listFiles(path, '.pem')

    certs = {}
    for fileName in fileNames:
        with open(fileName, 'r') as certFile:
            certs[fileName] = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certFile.read())
    return certs

def formatX509Name(x509Name):
    return ', '.join(['{}={}'.format(x, y) for x, y in x509Name.get_components()]).decode("iso8859")

#    https://tools.ietf.org/html/rfc5280#section-4.1.2.5.2
#    For the purposes of this profile, GeneralizedTime values MUST be
#    expressed in Greenwich Mean Time (Zulu) and MUST include seconds
#    (i.e., times are YYYYMMDDHHMMSSZ), even where the number of seconds
#    is zero.  GeneralizedTime values MUST NOT include fractional seconds.

def parseAsn1DateString(asn1Date):
    pattern = re.compile(
        r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(Z|(\+0{4}))$')
    match = re.match(pattern, asn1Date)
    if match is not None:
        groups = match.groupdict()
        return datetime(int(groups['year']),
                        int(groups['month']),
                        int(groups['day']),
                        int(groups['hour']),
                        int(groups['minute']),
                        int(groups['second']), 0).isoformat()
