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

def process(inputfile):
    with open(inputfile, 'rt') as f:
        piki = open("PIKI.seq", "wt")
        anders = open("ANDERS.seq", "wt")
        pilotit = open("PILOTIT.seq", "wt")
        vaski = open("VASKI.seq", "wt")
        record = []
        read = 0
        found = {"PIKI": 0, "ANDERS": 0, "VASKI": 0, "PILOTIT": 0}
        for line in f:
            if isRecordBoundary(line):
                if hasOwner(record, "PIKI"):
                    piki.write(''.join(record))
                    found["PIKI"] += 1
                if hasOwner(record, "ANDER"):
                    anders.write(''.join(record))
                    found["ANDERS"] += 1
                if hasOwner(record, "ANDER") or hasOwner(record, "PIKI"):
                    pilotit.write(''.join(record))
                    found["PILOTIT"] += 1
                if hasOwner(record, "VASKI"):
                    vaski.write(''.join(record))
                    found["VASKI"] += 1
                if read % 100000 == 0:
                    print(
                            "Read {0} records, found: \n" \
                            "Piki: {1} \n" \
                            "Anders: {2} \n" \
                            "Vaski: {3} \n" \
                            "pilotit: {4}".format(read, found["PIKI"],
                                found["ANDERS"], found["VASKI"],
                                found["PILOTIT"]))
                read += 1
                record = []
            record.append(line)
        piki.close()
        anders.close()
        pilotit.close()
        vaski.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store',
            dest='input',
            help='Inputfile')
    arguments = parser.parse_args()
    process(arguments.input)
