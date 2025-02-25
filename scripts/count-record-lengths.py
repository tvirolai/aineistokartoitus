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

def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f:
        out = open(outputfile, "wt")
        record = []
        read = 0
        lengths = {}
        for line in f:
            if isRecordBoundary(line) and record:
                length = recordLength(record)
                if length == 41 or length == 11:
                    print("Tietueen pituus: {0}".format(length))
                    printableRec = "".join([x for x in record if all(char.isdigit() for char in getTag(x)) or getTag(x) == "LDR"])
                    print(printableRec)
                # out.write("{0}\n".format(length))
                if length in lengths:
                    lengths[length] += 1
                else:
                    lengths[length] = 1
                if read % 100000 == 0:
                    print("Read {0} records, lengths:\n{1}".format(read, lengths))
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
