from pyasn1.codec.der import decoder
from pyasn1_modules import rfc3280

def decodeAsn1Extension(name, data):
    extensions = {
        'subjectAltName': extractSubjectAltNames
    }

    return extensions[name](data)

def extractSubjectAltNames(data):
    parsed = decoder.decode(data, asn1Spec=rfc3280.SubjectAltName())
    return [str(altName[2]) for altName in parsed[0] if altName[2] is not None]
    