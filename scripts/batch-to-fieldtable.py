import argparse


def getTag(line):
    return line[10:13]


def getContent(line):
    return line[18:]


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


def fieldCounts(record):
    fields = {
            "CAT": 0,
            "FMT": 0,
            "LDR": 0,
            "LOW": 0,
            "SID": 0,
            "020": 0,
            "022": 0,
            "024": 0,
            "080": 0,
            "082": 0,
            "083": 0,
            "084": 0,
            "098": 0,
            "100": 0,
            "110": 0,
            "111": 0,
            "130": 0,
            "240": 0,
            "245": 0,
            "250": 0,
            "260": 0,
            "263": 0,
            "264": 0,
            "336": 0,
            "337": 0,
            "338": 0,
            "440": 0,
            "490": 0,
            "520": 0,
            "6XX": 0,
            "700": 0,
            "710": 0,
            "711": 0,
            "720": 0,
            "730": 0,
            "740": 0,
            "773": 0,
            "776": 0}
    for line in record:
        tag = getTag(line)
        if tag[0:1] == "6":
            fields["6XX"] += 1
        elif getTag(line) in fields:
            fields[getTag(line)] += 1
    return fields


def isNonsub(record):
    return len([x for x in record if getTag(x) == "773"]) == 0


def getId(record):
    return record[0][0:9]


def isRecordBoundary(line):
    return "FMT   L" in line


def process(inputfile, outputfile):
    with open(inputfile, 'rt') as f, open(outputfile, 'wt') as o:
        record = []
        read = 0
        # Print header
        cols = list(fieldCounts(record).keys())
        o.write(','.join(cols) + '\n')
        for line in f:
            if isRecordBoundary(line) and len(record) > 1:
                vals = [str(x) for x in fieldCounts(record).values()]
                o.write(','.join(vals) + '\n')
                if read % 100000 == 0 and read > 0:
                    print("Read {0} records." .format(read))
                read += 1
                record = []
            record.append(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input', help='Inputfile')
    parser.add_argument('-o', action='store', dest='output', help='Outputfile')
    arguments = parser.parse_args()
    process(arguments.input, arguments.output)
