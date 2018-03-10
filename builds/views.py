from pobuilds import app
from flask import request, render_template, redirect, url_for
from utils import *
import untangle
from constants import *

@app.route('/list')
def listbuilds():
    return "List of Builds"

@app.route('/import', methods=('GET', 'POST '))
def importBuild():
    print(request.args.get("message"))
    return render_template('home/import.html', message=request.args.get("message"))

@app.route('/parse', methods=('GET', 'POST'))
def parseBuild():

    if not request.form['pastebinURL']:
            return redirect(url_for('importBuild', message="Can't be empty"))

    # Grab the build data from Pastebin
    buildstring = cleanPastebin(request.form['pastebinURL'])

    # Parse the XML and convert to Python object
    buildxml = untangle.parse(decode(buildstring))

    # PlayerStat list from the untangled XML
    allstats = buildxml.PathOfBuilding.Build.PlayerStat
    # Subset of stats to display
    statsfilter = ["Spec:LifeInc", "AverageDamage", "Life", "Spec:ArmourInc"]
    # Use comprehension to look for the stats we're interested in
    statlist = {playerstat["stat"]:playerstat["value"] for playerstat in allstats if playerstat["stat"] in statsfilter}
    # Extract interesting metadata from the "Build" tag
    metadata = {
                "targetVersion": buildxml.PathOfBuilding.Build['targetVersion'].replace("_", "."),
                "className": buildxml.PathOfBuilding.Build['className'],
                "ascendClassName": buildxml.PathOfBuilding.Build['ascendClassName'],
                "bandit": buildxml.PathOfBuilding.Build['bandit'],
                "level": buildxml.PathOfBuilding.Build['level']
                }

    speclist = []
    # Untangle does some magic while creating the object so we need to
    # handle the case in which we're not dealing with a list
    if not isinstance(buildxml.PathOfBuilding.Tree.Spec, (list)):
        speclist.append(buildxml.PathOfBuilding.Tree.Spec)
    else:
        speclist = buildxml.PathOfBuilding.Tree.Spec

    # Create the list for 1 or more trees
    specs = {}
    for spec in speclist:
        specs[spec["title"]] = spec.URL.cdata.strip()
    print(specs)

    # Extract only the binary data from the trees URLs
    treedata = [v.strip().replace("https://www.pathofexile.com/passive-skill-tree/", "") for k, v in specs.items()]

    # Decode the payload of the longest tree in the list
    buildtree = decodeTree(max(treedata, key=len))

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

    builddata = {
                "stats":statlist,
                "metadata":metadata,
                "tree":specs,
                "notables":notablemap,
                "keystones":keystonemap
                }

    print("builddata", builddata)
    return render_template('builds/display_build.html', builddata=builddata)
