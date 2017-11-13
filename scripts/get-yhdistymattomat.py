import argparse

"""
Erotellaan dumpista PIKIn, ANDERSin, PILOTTIen ja VASKIn tietueet, jotka:
    1) Eivät yhdistyneet loadissa mihinkään (vain oman kirjaston tagi) tai
    2) eivät yhdistyneet toisiin yleisiin kirjastoihin
"""

def getTag(line):
    return line[10:13]


def getContent(line):
    return line[18:]


def getLowtags(record):
     return [x[21:].strip() for x in record if getTag(x) == "LOW"]

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
    tags = getLowtags(record)
    return len(tags) == 1 and lowtag in tags


def isRecordBoundary(line):
    return "FMT   L" in line


def isInOtherPublic(record, lowtag):
    tags = getLowtags(record)
    publicTagsInRec = [tag for tag in tags if tag in ["PIKI", "ANDER", "VASKI"]]
    return len(publicTagsInRec) > 1 and lowtag in tags


def hasOwner(record, lowtag):
    return lowtag in getLowtags(record)


def process(inputfile):
    with open(inputfile, 'rt') as f:
        PIKI_onlyowner = open("PIKI_onlyowner.seq", "wt")
        PIKI_onlypublic = open("PIKI_onlypublic.seq", "wt")
        ANDERS_onlyowner = open("ANDERS_onlyowner.seq", "wt")
        ANDERS_onlypublic = open("ANDERS_onlypublic.seq", "wt")
        VASKI_onlyowner = open("VASKI_onlyowner.seq", "wt")
        VASKI_onlypublic = open("VASKI_onlypublic.seq", "wt")
        record = []
        read = 0
        found = {"PIKI_onlyowner": 0,
                "PIKI_onlypublic": 0,
                "ANDERS_onlyowner": 0,
                "ANDERS_onlypublic": 0,
                "VASKI_onlyowner": 0,
                "VASKI_onlypublic": 0}
        for line in f:
            if isRecordBoundary(line):
                if isOnlyOwner(record, "PIKI"):
                    PIKI_onlyowner.write("".join(record))
                    found["PIKI_onlyowner"] += 1
                if not isInOtherPublic(record, "PIKI") and hasOwner(record, "PIKI"):
                    PIKI_onlypublic.write("".join(record))
                    found["PIKI_onlypublic"] += 1
                if isOnlyOwner(record, "ANDER"):
                    ANDERS_onlyowner.write("".join(record))
                    found["ANDERS_onlyowner"] += 1
                if not isInOtherPublic(record, "ANDER") and hasOwner(record, "ANDER"):
                    ANDERS_onlypublic.write("".join(record))
                    found["ANDERS_onlypublic"] += 1
                if isOnlyOwner(record, "VASKI"):
                    VASKI_onlyowner.write("".join(record))
                    found["VASKI_onlyowner"] += 1
                if not isInOtherPublic(record, "VASKI") and hasOwner(record, "VASKI"):
                    found["VASKI_onlypublic"] += 1
                    VASKI_onlypublic.write("".join(record))
                read += 1
                record = []
                if read % 100000 == 0:
                    print("Read {0} records, where:".format(read))
                    print("PIKI (only owner): {0}".format(found["PIKI_onlyowner"]))
                    print("PIKI (only public): {0}".format(found["PIKI_onlypublic"]))
                    print("ANDERS (only owner): {0}".format(found["ANDERS_onlyowner"]))
                    print("ANDERS (only public): {0}".format(found["ANDERS_onlypublic"]))
                    print("VASKI (only owner): {0}".format(found["VASKI_onlyowner"]))
                    print("VASKI (only public): {0}".format(found["VASKI_onlypublic"]))
                    print("=============================================")
            record.append(line)
        PIKI_onlyowner.close()
        PIKI_onlypublic.close()
        ANDERS_onlyowner.close()
        ANDERS_onlypublic.close()
        VASKI_onlyowner.close()
        VASKI_onlypublic.close()
        print("Read {0} records, where:".format(read))
        print("PIKI (only owner): {0}".format(found["PIKI_onlyowner"]))
        print("PIKI (only public): {0}".format(found["PIKI_onlypublic"]))
        print("ANDERS (only owner): {0}".format(found["ANDERS_onlyowner"]))
        print("ANDERS (only public): {0}".format(found["ANDERS_onlypublic"]))
        print("VASKI (only owner): {0}".format(found["VASKI_onlyowner"]))
        print("VASKI (only public): {0}".format(found["VASKI_onlypublic"]))
        print("=============================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store',
            dest='input',
            help='Inputfile')
    arguments = parser.parse_args()
    process(arguments.input)
