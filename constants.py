import re
import json
from urllib.request import urlopen

# Download passive skill tree URL
REGEX = re.compile(r"var\spassiveSkillTreeData\s+=\s+(\{.*\})")
TREEURL = "https://www.pathofexile.com/passive-skill-tree"
TREEPAGE = urlopen(TREEURL).read().decode('UTF-8')
PASSIVETREEJSON = REGEX.search(TREEPAGE).group(1)
PASSIVETREEDATA = json.loads(PASSIVETREEJSON)
PASSIVETREENODELIST = PASSIVETREEDATA["nodes"]
