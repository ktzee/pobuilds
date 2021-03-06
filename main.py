import untangle
from urllib.request import urlopen
from BuildTree import BuildTree
from utils import *
from pprint import pprint
import sys
import re
import json

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

# Download passive skill tree URL
regex = re.compile(r"var\spassiveSkillTreeData\s+=\s+(\{.*\})")
treeURL = "https://www.pathofexile.com/passive-skill-tree"
treePage = urlopen(treeURL).read().decode('UTF-8')
passiveTreeJson = regex.search(treePage).group(1)
passiveTreeData = json.loads(passiveTreeJson)
passiveTreeNodelist = passiveTreeData["nodes"]

# Use untangle to parse the XML
doc = untangle.parse(xml)

# PlayerStat list from the XML
statlist = doc.PathOfBuilding.Build.PlayerStat

# Output of the stats:
print("This build was made for: " + doc.PathOfBuilding.Build['targetVersion'].replace("_", "."))
print("Class Used: " + doc.PathOfBuilding.Build['className'])
print("Ascendancy: " + doc.PathOfBuilding.Build['ascendClassName'])
print("Bandit Choice: " + doc.PathOfBuilding.Build['bandit'])
print("Life Increased %: " + findStat(statlist, "Spec:LifeInc"))

# SPECS/TREES
# Dictionary of "Tree Name : Tree URL"
specs = {}
for spec in doc.PathOfBuilding.Tree.Spec:
    specs[spec["title"]] = spec.URL.cdata.strip()
# List containing all payloads from all URLs
treedata = [v.strip().replace("https://www.pathofexile.com/passive-skill-tree/", "") for k, v in specs.items()]
# We decode the largest payload (probably highest level tree)
buildTree = decodeTree(max(treedata, key=len))

# UNIQUES
itemdict = parseItems(doc.PathOfBuilding.Items.Item)
uniques = [v["item_name"] for k, v in itemdict.items() if v["rarity"] == "UNIQUE"]

# GEMS
gemsdict = parseGems(doc.PathOfBuilding.Skills.Skill)

print("================")
print("List of Keystone Nodes:")
print("================")
keystoneMap = []
for nodeId in buildTree.nodes:
    node = findNode(passiveTreeNodelist, nodeId)
    if node['ks']:
        keystoneMap.append(node)

for keystone in keystoneMap:
    print(keystone['dn'])
    print(keystone['icon'])
print("================")
print("List of Notable Nodes:")
print("================")
notableMap = []
for nodeId in buildTree.nodes:
    node = findNode(passiveTreeNodelist, nodeId)
    if node['not']:
        notableMap.append(node)

for notable in notableMap:
    print(notable['dn'])
    # Print the notable bonuses
    # print(notable['sd'])
print("================")
print("List of Uniques:")
print("================")
print(uniques)
print("================")
print("List of Gems:")
print("================")
for slot in gemsdict:
    print(slot)
    for gem in gemsdict[slot]:
        print("|")
        print("->", gem[0], "LVL:", gem[1])