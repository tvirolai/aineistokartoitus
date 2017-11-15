import argparse

"""
Laske tieto- ja kaunokirjallisuuden määrät.

Kriteerit:

    1) kaunokirjallisuus: FMT = BK ja ykl-luokitus on väliltä 80-85
    2) tietokirjallisuus: FMT = BK ja ykl-luokitus ei ole väliltä 80-85

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


def isLiterature(record):
    FMT = [field for field in record if getTag(field) == "FMT"]
    return "BK" in FMT.pop()


def getYKL(record):
    """
    Return a list of YKL codes in record.
    """
    return [getContent(x).strip().split("$$")[1][1:] for x in record if getTag(x) == "084"]


def hasYkl(record):
    return len(getYKL(record)) > 0


def isFiction(record):
    # Try to convert values to floats
    f084_floats = []
    for code in getYKL(record):
        try:
            f084_floats.append(float(code))
        except:
            pass
    fictionCodes = [code for code in f084_floats if code > 80.0 and code < 86.0]
    return True if fictionCodes else False


def process(inputfile):
    with open(inputfile, 'rt') as f:
        record = []
        read = 0
        found = {"tieto": 0, "kauno": 0, "ei luokitusta": 0}
        for line in f:
            if isRecordBoundary(line) and record:
                if isLiterature(record):
                    if not hasYkl(record):
                        # print("".join(record))
                        found["ei luokitusta"] += 1
                    else:
                        if isFiction(record):
                            found["kauno"] += 1
                        else:
                            found["tieto"] += 1
                if read % 100000 == 0:
                    print("Luettu {0} tietuetta.\n" \
                          "Kaunokirjallisuus: {1}\n" \
                          "tietokirjallisuus: {2}\n" \
                          "ei YKL-luokitusta: {3}".format(
                              read, found["kauno"], found["tieto"],
                              found["ei luokitusta"]))
                read += 1
                record = []
            record.append(line)
        print("Luettu {0} tietuetta.\n" \
              "Kaunokirjallisuus: {1}\n" \
              "tietokirjallisuus: {2}\n" \
              "ei YKL-luokitusta: {3}".format(
                  read, found["kauno"], found["tieto"],
                  found["ei luokitusta"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store',
            dest='input',
            help='Inputfile')
    arguments = parser.parse_args()
    process(arguments.input)
