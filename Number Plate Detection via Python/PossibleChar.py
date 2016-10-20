

# ---------------------------------- UKLJUČIVANJE MODULA -------------------------
import cv2
import numpy as np
import math
# -------------------------------------------------------------------------------

# Poziva se iz skipte DetectPLates
class PossibleChar:

    def __init__(self, _contour):
        self.contour = _contour

        self.boundingRect = cv2.boundingRect(self.contour)

        # FUNKCIJA CV KOJA RAČUNA ISHODIŠTE KONTURE TE VISINU I ŠIRINU
        [intX, intY, intWidth, intHeight] = self.boundingRect

        # IZVALAČENJE PODATAKA U 4 VRIJEDNOSTI
        self.intBoundingRectX = intX
        self.intBoundingRectY = intY
        self.intBoundingRectWidth = intWidth
        self.intBoundingRectHeight = intHeight

        # RAČUNANJE VELIČINE PRAVOKUTNIKA, ODNOSNO VELIČINE KONTURE
        self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight


        # RAČUNANJE SREDIŠTA KONTURE
        self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
        self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2

        # RAČUNANJE VELIČINE DIJAGONALE KONTURE
        self.fltDiagonalSize = math.sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2))

        # INDEKS VELIČINE ???????  OMJER VISINE I ŠIRINE
        self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight)









