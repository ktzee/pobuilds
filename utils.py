import base64
import zlib
import struct
import json
from urllib.request import urlopen
import re
from BuildTree import BuildTree
import pdb


# Accepts a raw encoded string as argument, it replaces all "-" with "+" and all "_" with "/" and returns a decoded and decompressed string
def decode(rawstring):
    return zlib.decompress(base64.b64decode(rawstring.replace("-", "+").replace("_", "/"))).decode('UTF-8')

def decodeTree(treestring):
    #AAAABAIBAFuvFHWNub3mFyZV4M2YAx7BoAUtbIx4GU4qo4pYWpu1RfQV9v66WhofQQ5IPL5VS3TtI_a-pwzyR35ieejWCC5_xp2qeoSpeS5T5Grtgyo4pcth4upi034k_ZoXkoBfcF3y_97vj8jMES967311df3QrY1973oNjRa_pMI31P1ujYEAXt9vFf3BxbIZQzHC7L02QdDnVIGsPs9Nku4OdcvWB4o4wzrawdvnEZZSKY1-h3btP29XIuqbjetj_MVKfWSvNj2DbTIBYqxlTSsKAAYzkn8rjb_Y1UMTTP_UQhmO1COExed0z3oFtTB8tMXDM7VIUUfTbyaVePl-3YRvk5A=
    rawdata = base64.b64decode(treestring.replace("-", "+").replace("_", "/"))
    tree = BuildTree()
    # unpack will always return a tuple. We're saving only the first element in the tuple.
    tree.version = struct.unpack_from(">I", rawdata, 0)[0]
    tree.classId = struct.unpack_from(">B", rawdata, 4)[0]
    tree.ascendClassId = struct.unpack_from(">B", rawdata, 5)[0]
    # position 6 is a "0" separator
    total = (len(rawdata)-7)//2
    tree.nodes = struct.unpack_from(">"+"H"*total, rawdata,7)
    return tree

# Function to look for specific stats in the PlayerStat list
def findStat(statlist, stat):
    for item in statlist:
        if item['stat'] == stat:
            return(item['value'])

def findNode(nodelist, buildnode):
    for node in nodelist:
        if node['id'] == buildnode:
            return node

def cleanPastebin(pastebin):
    return urlopen(pastebin.replace("pastebin.com/", "pastebin.com/raw/")).read().decode('UTF-8')

def parseItems(itemlist):
    itemdict = {}
    for item in itemlist:
        itemfacts = item.cdata.strip().split("\n")
        itemdict[item["id"]] = {
            "variant":item["variant"],
            "rarity":itemfacts[0].replace("Rarity: ", ""),
            "item_name":itemfacts[1],
            "item_type":itemfacts[2],
            "level_req":itemfacts[7].replace("LevelReq: ", "")
        }

    return itemdict


def parseGems(gemlist):
    gemsdict = {}
    for skill in gemlist:
        if skill["enabled"] == 'true' and not skill["source"]:
            for gem in skill.Gem:
                print(gem)
                if gem["enabled"] == "true":
                    if skill["slot"] in gemsdict:
                        gemsdict[skill["slot"]].append([gem["nameSpec"], gem["level"]])
                    else:
                        gemsdict[skill["slot"]] = [[gem["nameSpec"], gem["level"]]]
    return gemsdict
    
# should be modified to directly accept a json
def loadPoeTree():
    # page containing the json
    treeURL = "https://www.pathofexile.com/passive-skill-tree"

    # regex to extract the json from the variable in the page source
    regex = re.compile(r"var\spassiveSkillTreeData\s+=\s+(\{.*\})")

    # Download passive skill tree URL
    treePage = urlopen(treeURL).read().decode('UTF-8')
    passiveTreeJson = regex.search(treePage).group(1)
    passiveTreeData = json.loads(passiveTreeJson)
    passiveTreeNodelist = passiveTreeData["nodes"]

    return passiveTreeNodelist
