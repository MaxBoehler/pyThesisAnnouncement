def readContent(conf):
    confContent = {"intro": False,
                   "leftColumn": False,
                   "rightColumn": False,}
    conf.seek(0,0)
    content = conf.read()

    introStart = "beginIntroduction["
    introEnd = "]endIntroduction"
    intro = content[content.find(introStart)+len(introStart):content.find(introEnd)].strip()
    if intro != "":
        confContent["intro"] = intro

    leftColStart = "beginLeftColumn["
    leftColEnd = "]endLeftColumn"
    leftColumn = content[content.find(leftColStart)+len(leftColStart):content.find(leftColEnd)].strip()
    if leftColumn != "":
        confContent["leftColumn"] = leftColumn

    rightColStart = "beginRightColumn["
    rightColEnd = "]endRightColumn"
    rightColumn = content[content.find(rightColStart)+len(rightColStart):content.find(rightColEnd)].strip()
    if rightColumn != "":
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

    if confVars["colorTheme"] == False:
        raise ValueError("Please insert a colorTheme")

    elif confVars["mainTitle"] == False:
        raise ValueError("Please insert a mainTitle")

    elif confVars["intro"] == False:
        raise ValueError("Empty introduction text.")

    elif confVars["leftColumn"] == False:
        raise ValueError("Your content for the left column appears to be emtpy.")

    elif confVars["rightColumn"] == False:
        raise ValueError("Your content for the right column appears to be emtpy.")

    conf.close()
    return confVars
