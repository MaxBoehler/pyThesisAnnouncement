import numpy as np
import glob
from PIL import Image
import os


class header:

    def __init__(self, width, height):
        self.headerWidth = width
        self.headerHeight = height


        self.absPath = os.getcwd()
        self.headerPath = os.path.join(self.absPath, *["tex", "img", "header.png"])
        self.pathMask = os.path.join(self.absPath, *["pyThesisAnnouncement", "templates", "images", "mask.png"])

    def aspectRatioWidth(self,width,height,newHeight):
        heightFraction = (1/height)*newHeight
        newWidth = width * heightFraction

        return newWidth


    def loadFiles(self, path):
        filePath = []
        for i in glob.glob(os.path.join(path, "*")):
            filePath.append(i)
        filesOriginal  = [ Image.open(i) for i in filePath ]

        return filesOriginal


    def resizeOriginals(self, originals, resizedHeight):
        filesResized = []
        totalWidth = 0
        for i in originals:
            width = i.size[0]
            height = i.size[1]

            resizedWidth = self.aspectRatioWidth(width,height,resizedHeight)
            filesResized.append(i.resize((int(resizedWidth),resizedHeight)))

            totalWidth += resizedWidth

        return filesResized, totalWidth

    def createPlainHeader(self, filesResized, totalWidth, resizedHeight):
        header = Image.new('RGB', (int(totalWidth), resizedHeight))
        xOffset = 0
        for i in filesResized:
            header.paste(i, (xOffset,0))
            xOffset += i.size[0]

        if totalWidth > self.headerWidth :
            print("\033[93mWarning: Header is wider than {}px -> Cropping\033[0m".format(self.headerWidth))
            cutOff = (totalWidth - self.headerWidth ) / 2
            header = header.crop((cutOff, 0, totalWidth - cutOff, self.headerHeight))

        print("Saving header: " + str(self.headerPath))
        header.save(self.headerPath)

    def createMaskedHeader(self):
        header = Image.open(self.headerPath).convert("RGBA")
        mask = Image.open(self.pathMask).convert("RGBA")

        if mask.size[1] != header.size[1]:
            mask = mask.resize((header.size[0], header.size[1]))

        header.paste(mask, (0, 0), mask)
        header.save(self.headerPath)

    def insertLogos(self, logos, resizedHeight, spaceBetweenLogos):
        header = Image.open(self.headerPath).convert("RGBA")
        xOffset = self.headerWidth - 50 + spaceBetweenLogos
        for l in logos:
            width = l.size[0]
            xOffset -= width + spaceBetweenLogos
            offset = ((xOffset, self.headerHeight-resizedHeight))
            header.paste(l, offset)

        header.save(self.headerPath)
