import base64
import zlib
import struct
from BuildTree import BuildTree


# Accepts a raw encoded string as argument, it replaces all "-" with "+" and all "_" with "/" and returns a decoded and decompressed string
def decode(rawstring):
    return zlib.decompress(base64.b64decode(rawstring.replace("-", "+").replace("_", "/"))).decode('UTF-8')

def decodetree(treestring):
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
def findstat(statlist, stat):
    for item in statlist:
        if item['stat'] == stat:
            return(item['value'])
