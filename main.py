import untangle
from urllib.request import urlopen
from BuildTree import BuildTree
from utils import *
from pprint import pprint
import sys

# https://pastebin.com/ZBQHAF2U
# ("Insert an import string or a Pastebin URL: ")
rawstring = sys.argv[1]

if "pastebin.com/" in rawstring:
    rawstring = urlopen(rawstring.replace("pastebin.com/", "pastebin.com/raw/")).read().decode('UTF-8')

# Save resulting XML into a variable
xml = decode(rawstring)

# Write-to-file for debugging purposes
outputfile = open('data.xml', 'w')
outputfile.write(xml)
outputfile.close()

# Use untangle to parse the XML
doc = untangle.parse(xml)

# PlayerStat list from the XML
statlist = doc.PathOfBuilding.Build.PlayerStat

# Output of the stats:
print("This build was made for: " + doc.PathOfBuilding.Build['targetVersion'].replace("_", "."))
print("Class Used: " + doc.PathOfBuilding.Build['className'])
print("Ascendancy: " + doc.PathOfBuilding.Build['ascendClassName'])
print("Bandit Choice: " + doc.PathOfBuilding.Build['bandit'])
print("Life Increased %: " + findstat(statlist, "Spec:LifeInc"))

treedata = []
for spec in doc.PathOfBuilding.Tree.Spec[0:3]:
    print(spec["title"])
    print(spec.URL.cdata.strip())
    treedata.append(spec.URL.cdata.strip().replace("https://www.pathofexile.com/passive-skill-tree/", ""))

# pprint(vars(decodetree(treedata[0])))
