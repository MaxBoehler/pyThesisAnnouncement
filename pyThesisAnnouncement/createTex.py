import os
from shutil import copyfile
import glob

def addTitle(mainTitle, subTitle):
    rawStr = "\\textbf{" + mainTitle + "}\\\\\n"
    if subTitle:
        if len(subTitle) < 49:
            rawStr += "\\rule{\\textwidth}{1.0pt}\\\\[0.4cm]\n"
            rawStr += subTitle + "\n"
            height = "4cm"
        elif len(subTitle) > 98:
            raise ValueError("Subtitle is too long. Maximal length is 98 characters")
        else:
            subTitle1 = []
            subTitle2 = []
            counter = 0
            subTitle = subTitle.split(" ")
            # Whoever reads this, I am deeply sorry for the loop below.
            # But time is short and I need to finish....
            for i in range(len(subTitle)):
                if i < len(subTitle) - 1:
                    checkCounter = counter + len(subTitle[i+1])
                else:
                    checkCounter = 49
                if not checkCounter >= 49:
                    counter += len(subTitle[i])
                    subTitle1.append(subTitle[i])
                else:
                    subTitle2.append(subTitle[i])

            rawStr += "\\rule{\\textwidth}{1.0pt}\\\\[0.4cm]\n"
            rawStr += " ".join(subTitle1) + "\\\\[0.4cm]\n"
            rawStr += " ".join(subTitle2)
            height = "4.6cm"

    else:
        height = "2cm"

    return rawStr, height

def addContact(name, webpage, mail, place):
    rawStr = ""
    if name:
        rawStr += "\\includegraphics[width=0.3cm]{img/person.pdf} " + name + " \\hspace{0.3cm}\n"
    if webpage:
        rawStr += "\\includegraphics[width=0.3cm]{img/www.pdf} " + webpage + " \\hspace{0.3cm}\n"
    if mail:
        rawStr += "\\includegraphics[width=0.3cm]{img/mail.pdf} " + mail + " \\hspace{0.3cm}\n"
    if place:
        rawStr += "\\includegraphics[width=0.3cm]{img/place.pdf} " + place + " \\hspace{0.3cm}\n"

    rawStr = rawStr[:-15]
    return rawStr

def distributeGraphics():
    for file in glob.glob("pyThesisAnnouncement/templates/images/*.pdf"):
        copyfile(file, "tex/img/"+file.split("/")[-1])

def createTex(confVars, texPath):
    templateOrigin = open("pyThesisAnnouncement/templates/tex/template.tex", "r")
    templateOriginRaw = templateOrigin.read()
    templateOrigin.close()

    if not os.path.isfile(os.path.join(texPath, "thesisAnnoucement.tex")):
        template = open(os.path.join(texPath, "thesisAnnoucement.tex"), "w+")
    else:
        raise FileExistsError("Can not create LaTeX file since tex/thesisAnnoucement.tex exists. Please remove or move this file.")

    title, titleHeight = addTitle(confVars["mainTitle"], confVars["subTitle"])
    contact = addContact(confVars["name"],confVars["webpage"],\
                         confVars["mail"],confVars["place"])

    templateOriginRaw = templateOriginRaw.replace("%%TYPE%%", confVars["type"])
    templateOriginRaw = templateOriginRaw.replace("%%COLORTHEME%%", confVars["colorTheme"])
    templateOriginRaw = templateOriginRaw.replace("%%TITLEHEIGHT%%", titleHeight)
    templateOriginRaw = templateOriginRaw.replace("%%TITLE%%", title)
    templateOriginRaw = templateOriginRaw.replace("%%INTRO%%", confVars["intro"])
    templateOriginRaw = templateOriginRaw.replace("%%LEFTCOLUMN%%", confVars["leftColumn"])
    templateOriginRaw = templateOriginRaw.replace("%%RIGHTCOLUMN%%", confVars["rightColumn"])
    templateOriginRaw = templateOriginRaw.replace("%%CONTACT%%", contact)

    template.write(templateOriginRaw)

    template.close()
