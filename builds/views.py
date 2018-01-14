from pobuilds import app
from flask import request, render_template
from utils import *
import untangle
from constants import *

@app.route('/list')
def list():
    return "List of Builds"


@app.route('/parse', methods=('GET', 'POST'))
def parseBuild():
    buildstring = cleanPastebin(request.form['pastebinURL'])

    buildxml = untangle.parse(decode(buildstring))

    # PlayerStat list from the XML
    allstats = buildxml.PathOfBuilding.Build.PlayerStat
    # Stats to display
    displaystats = ["Spec:LifeInc", "AverageDamage", "Life", "Spec:ArmourInc"]
    # Use comprehension to look for the stats we're interested in
    statlist = {playerstat["stat"]:playerstat["value"] for playerstat in allstats if playerstat["stat"] in displaystats}

    # Same thing with SkillSelect
    allskills = buildxml.PathOfBuilding.Skills
    skillslist = {skill["slot"]:skill.Gem for skill in allskills if skill["enabled"] == "true"}
    print(skillslist)

    # Extract the first 3 trees from the build and grab their payload
    treedata = []
    for spec in buildxml.PathOfBuilding.Tree.Spec[0:3]:
        print(spec["title"])
        print(spec.URL.cdata.strip())
        treedata.append(spec.URL.cdata.strip().replace("https://www.pathofexile.com/passive-skill-tree/", ""))

    # Decode the payload of the first tree in the list
    buildtree = decodeTree(treedata[0])

    # Create a map of keystones used in the build
    keystonemap = []
    for nodeid in buildtree.nodes:
        node = findNode(PASSIVETREENODELIST, nodeid)
        if node['ks']:
            keystonemap.append(node)

    # Create a map of notables used in the build
    notablemap = []
    for nodeid in buildtree.nodes:
        node = findNode(PASSIVETREENODELIST, nodeid)
        if node['not']:
            notablemap.append(node)

    return render_template('builds/display_build.html', buildxml=buildxml, statlist=statlist, keystonemap=keystonemap, notablemap=notablemap)
