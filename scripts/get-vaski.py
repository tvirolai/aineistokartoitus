import argparse

def getTag(line):
    return line[10:13]

def getContent(line):
    return line[18:]

def hasOwner(record, lowtag):
    return list(filter(lambda x: getTag(x) == "LOW" and lowtag in
        getContent(x), record))

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

def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f:
        o = open(outputfile, "wt")
        record = []
        read = 0
        found = 0
        for line in f:
            if isRecordBoundary(line):
                if hasOwner(record, "VASKI"):
                    o.write(''.join(record))
                    o.write("\n")
                    found += 1
                if read % 500000 == 0:
                    print(
                    "Read {0} records, Vaski: {1}".format(read, found))
                read += 1
                record = []
            record.append(line)
        o.close()

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
