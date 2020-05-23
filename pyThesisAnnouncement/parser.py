def readContent(conf):
    confContent = {"intro": False,
                   "leftColumn": False,
                   "rightColumn": False,}
    conf.seek(0,0)
    content = conf.read()

    introStart = "beginIntroduction["
    introEnd = "]endIntroduction"
    intro = content[content.find(introStart)+len(introStart):content.find(introEnd)]

    leftColStart = "beginLeftColumn["
    leftColEnd = "]endLeftColumn"
    leftColumn = content[content.find(leftColStart)+len(leftColStart):content.find(leftColEnd)]

    rightColStart = "beginRightColumn["
    rightColEnd = "]endRightColumn"
    rightColumn = content[content.find(rightColStart)+len(rightColStart):content.find(rightColEnd)]

    confContent["intro"] = intro
    confContent["leftColumn"] = leftColumn
    confContent["rightColumn"] = rightColumn

    return confContent

def readConf(confPath):
    conf = open(confPath, "r")

    confVars = {"type": False, \
                "colorTheme": False, \
                "mainTitle": False, \
                "subTitle": False, \
                "name": False, \
                "webpage": False, \
                "mail": False, \
                "place": False }
    for line in conf:
        commentLine = False
        line = line.strip()
        for i in line:
            if i == "#":
                commentLine = True
                break
        if not commentLine and line != "":
            var = line.split("=")[0].strip()
            val = line.split("=")[-1].strip()
            if val != "" and var in confVars.keys():
                confVars[var] = val

    confVars = {**confVars, **readContent(conf)}

    if confVars["colorTheme"] == None:
        raise ValueError("Please insert a colorTheme")

    if confVars["mainTitle"] == None:
        raise ValueError("Please insert a mainTitle")

    conf.close()
    return confVars
