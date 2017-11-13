import argparse

def getTag(line):
    return line[10:13]


def getContent(line):
    return line[18:]


def isNonsub(record):
    return len([x for x in record if getTag(x) == "773"]) == 0


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


def isOnlyOwner(record, lowtag):
    lowFields = [x for x in record if getTag(x) == "LOW"]
    return len(lowFields) == 1


def isRecordBoundary(line):
    return "FMT   L" in line

def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f, open(outputfile, 'wt') as o:
        record = []
        read = 0
        found = 0
        found_nonsub = 0
        for line in f:
            if isRecordBoundary(line):
                if isOnlyOwner(record, "VASKI"):
                    o.write(''.join(record))
                    found += 1
                    if isNonsub(record):
                        found_nonsub += 1
                    if found % 100 == 0:
                        print("Found {0} recs ({1} non-subrecords) owned only "
                                "by VASKI ({2} records read)".format(found,
                                    found_nonsub, read))
                read += 1
                record = []
            record.append(line)
        print("Total: {0} only Vaski, of which {1} non-sub".format(found,
            found_nonsub))

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
