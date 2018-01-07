import base64
from urllib.request import urlopen
import zlib
import untangle

# https://pastebin.com/ZBQHAF2U
rawstring = input("Insert an import string or a Pastebin URL: ")

if "pastebin.com/" in rawstring:
    rawstring = urlopen(rawstring.replace("pastebin.com/", "pastebin.com/raw/")).read().decode('UTF-8')

# Accepts a raw encoded string as argument, it replaces all "-" with "+" and all "_" with "/" and returns a decoded and decompressed string
def decode(rawstring):
    return zlib.decompress(base64.b64decode(rawstring.replace("-", "+").replace("_", "/"))).decode('UTF-8')

# Save resulting XML into a variable
xml = decode(rawstring)

# Write-to-file for debugging purposes
outputfile = open('data.xml', 'w')
outputfile.write(xml)
outputfile.close()

# Use untangle to parse the XML
doc = untangle.parse(xml)

# Function to look for specific stats in the PlayerStat list
def findstat(statlist, stat):
    for item in statlist:
        if item['stat'] == stat:
            return(item['value'])

# PlayerStat list from the XML
statlist = doc.PathOfBuilding.Build.PlayerStat

# Output of the stats:
print("This build was made for: " + doc.PathOfBuilding.Build['targetVersion'].replace("_", "."))
print("Class Used: " + doc.PathOfBuilding.Build['className'])
print("Ascendancy: " + doc.PathOfBuilding.Build['ascendClassName'])
print("Bandit Choice: " + doc.PathOfBuilding.Build['bandit'])
print("Life Increased %: " + findstat(statlist, "Spec:LifeInc"))
#print("Total DPS: " + findstat(statlist, "TotalDPS"))
