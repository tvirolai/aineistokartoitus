import argparse

"""
Read a batch of records and count the length (the number of fields) in each.
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

def recordLength(record):
    """
    Return the number of fields in record. Internal fields or leader are not
    included in the length.
    """
    return len([x for x in record if all(char.isdigit() for char in getTag(x))])


def headingsInField(field):
    return [x[1:].strip() for x in field.split("$$") if len(x) > 0 and x[:1].isalpha()]

def getSubjectHeadings(record):
    f6XX = [headingsInField(x) for x in record if getTag(x)[:1] == "6"]
    return [x for sublist in f6XX for x in sublist]


def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f:
        out = open(outputfile, "wt")
        record = []
        read = 0
        lengths = {}
        for line in f:
            if isRecordBoundary(line) and record:
                sfs = getSubjectHeadings(record)
                if sfs:
                    out.write("\n".join(sfs) + "\n")
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
