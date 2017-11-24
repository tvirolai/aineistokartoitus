import argparse

"""
Etsi tietueet, joissa on muiden(kin) kuin yleisten kirjastojen tunnukset.
"""

def getTag(line):
    return line[10:13]

def getContent(line):
    return line[18:]

def hasOwner(record, lowtag):
    return list(filter(lambda x: getTag(x) == "LOW" and lowtag in
        getContent(x), record))

def getId(record):
    if len(record) > 0:
        return record[0][:9]


def getOwners(record):
    # Return a list of LOW-tags in record.
    return [x[21:-1] for x in record if getTag(x) == "LOW"]

def isEmaterial(record):
    """
    A record is classified as e-material if 008/23 = 'o' and 007/1 = 'r'

    """
    fields = [x for x in record if getTag(x) in ["007", "008"]]
    f007 = list(filter(lambda x: getTag(x) == "007" and getContent(x)[1:2] ==
        'r', fields))
    f008 = list(filter(lambda x: getTag(x) == "008" and getContent(x)[23:24] ==
        'o', fields))
    if len(f007) > 0 and len(f008) > 0:
        return True
    return False

def isRecordBoundary(line):
    return "FMT   L" in line


def getFormatCode(record):
    return record[0][18:]

def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f:
        out = open(outputfile, "wt")
        record = []
        read = 0
        found = 0
        tags = {"PIKI": 0, "ANDER": 0, "VASKI": 0, "KUOPI": 0}
        for line in f:
            if isRecordBoundary(line) and record:
                print(getFormatCode(record))
                found += 1
                if read % 500000 == 0:
                    print(
                    "Read {0} records, muu Melinda: {1}".format(read, found))
                read += 1
                record = []
            record.append(line)
        out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store',
            dest='input',
            help='Inputfile')
    parser.add_argument('-o', action='store',
            dest='output',
            help='Outputfile')
    arguments = parser.parse_args()
    process(arguments.input, arguments.output)
