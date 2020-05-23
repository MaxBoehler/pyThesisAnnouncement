import sys
import os
import time

def welcomeMsg():
    print()
    print("################################################")
    print("         \033[1m\033[92mPyThesisTemplate \033[0mVersion 1.0")
    print("################################################")
    print("Author: Max Boehler")
    print()

if __name__ == "__main__":
    welcomeMsg()
    try:
        from pyThesisAnnouncement import tools
        from pyThesisAnnouncement import header
        from pyThesisAnnouncement import parser
        from pyThesisAnnouncement import createTex
        print("\033[92mStartup successful\033[0m\n")
    except ImportError as e:
        print("\033[91mError at starting up:\033[0m " + str(e))
        sys.exit()

    try:
        tools.checkExecutable("pdflatex")
        LaTeXCheck = True
    except Exception as e:
        LaTeXCheck = False
        print("\033[93mLaTeX Warning:\033[0m " + str(e) + "\n")
        print("LaTex file will be created, but PDF file can not be created with this script.")
        print("Pleas compile the LaTeX file by yourself!\n")
        time.sleep(2)

    print("Prechecking files .... ")
    try:
        absPath = os.getcwd()
        for f in ["images", "logos", "tex"]:
            tools.prechecking(f,True)
            print(f + "/ \033[92mpassed\033[0m ")
        tools.prechecking("conf",False)
        print("conf \033[92mpassed\033[0m ")
    except FileNotFoundError as e:
        print(f + " \033[91mfailed\033[0m ")
        print("\033[91mError while prechecking:\033[0m " + str(e))
        sys.exit()
    except Exception as e:
        print("\033[91mPrechecking failed:\033[0m " + str(e))
        sys.exit()

    try:
        confPath = 'conf'
        confVars = parser.readConf(confPath)
        print("\n\033[92mConfig file read!\033[0m")
    except Exception as e:
        print("\033[91mError while reading config file:\033[0m " + str(e))
        sys.exit()

    try:
        createTex.createTex(confVars, os.path.join(absPath, "tex"))
        createTex.distributeGraphics()
        print("\n\033[92mLaTeX file created!\033[0m")
    except Exception as e:
        print("\033[91mError while creating the tex file:\033[0m " + str(e))
        sys.exit()

    print("\nCreating Header ....")
    try:
        headerHeight = 700
        headerWidth = 2500
        logoHeight = 220
        spaceBetweenLogos = 50

        header = header.header(headerWidth, headerHeight)
        print("Loading images ....")
        imagesOriginal = header.loadFiles(os.path.join(absPath, "images"))
        print("Creating logos ....")
        logosOriginal = header.loadFiles(os.path.join(absPath, "logos"))

        print("Resizing images -> new height = {}px".format(headerHeight))
        imagesResized, imagesTotalWidth = header.resizeOriginals(imagesOriginal,headerHeight)
        print("Resizing logos -> new height = {}px".format(logoHeight))
        logosResized, logosTotalWidth = header.resizeOriginals(logosOriginal,logoHeight)

        # Checking if Logos are larger in height then the mask.
        # The mask is a straight line. Therefore check if logo height is larger
        # than the y-value at the x position of the logo
        xLogo = headerWidth - logosTotalWidth
        yMask = headerHeight + tools.calcMask(headerWidth,0,headerHeight, headerHeight*0.7,-headerHeight,xLogo)

        while logoHeight > yMask * 0.8: # puffer of 20%
            logoHeight -= 10
            print("Logos are wider then allowed -> resizing with new height = {}px".format(logoHeight))
            logosResized, logosTotalWidth = header.resizeOriginals(logosOriginal,logoHeight)
            xLogo = headerWidth - logosTotalWidth
            yMask = headerHeight + tools.calcMask(headerWidth,0,headerHeight, headerHeight*0.7,-headerHeight,xLogo)

        print("Creating plain header ....")
        header.createPlainHeader(imagesResized, imagesTotalWidth, headerHeight)
        print("Adding mask ....")
        header.createMaskedHeader()
        print("Inserting logos ....")
        header.insertLogos(logosResized, logoHeight, spaceBetweenLogos)

        print("\n\033[92mHeader created!\033[0m\n")
    except Exception as e:
        print("\033[91mError while creating header:\033[0m " + str(e))
        sys.exit()


    try:
        if LaTeXCheck:
            print("Create PDF file ...")
            dir = os.path.join(absPath, "tex")
            latexCommand = "pdflatex --interaction=nonstopmode thesisAnnoucement.tex"
            rmCommand = "rm thesisAnnoucement.aux thesisAnnoucement.log"
            tools.shellCommand(dir, latexCommand)
            tools.shellCommand(dir, rmCommand)
            print("\n\033[92mPDF file created created!\033[0m\n")
    except Exception as e:
        print("\n\033[91mError while creating PDF file with pdflatex:\033[0m\n" + str(e))

    print("\n\033[1m\033[92mAnnouncement succesful created!\033[0m")
    if LaTeXCheck:
        print("\n")
    else:
        print("(Since pdflatex was not found on your system, only the LaTeX file was created!)\n\n")
