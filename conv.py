
import csv, json
from json2xml import json2xml, readfromstring

def insertHeader():
    pass

def conv(csvFile,xmlFile):
    with open(csvFile, "r") as cf:
        fieldnames = tuple(cf.readline().split(','))

        reader = csv.DictReader(cf, fieldnames)
        json_csv = json.dumps([row for row in reader])

    with open(xmlFile, "w") as xf:
        insertHeader()
        data = readfromstring(json_csv)
        xf.write(json2xml.Json2xml(data, wrapper="row", indent=4).to_xml())


