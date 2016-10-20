
# ---------------------------------- UKLJUČIVANJE MODULA -------------------------
import cv2
import numpy as np
import math
import random
# -------------------------------------------------------------------------------


# -------------------------------- UKLJUČIVANJE VANJSKIH SKRIPTI --------------
import Main
import Preprocess
import PossibleChar
import Determination as det
# -------------------------------------------------------------------------------

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

# ----------------------------------------------------------------------------------------------------------------
# Pozivanje ove funkcije iz skripte DetectPlates
def checkIfPossibleChar(possibleChar):

    # U funckiju dolazi varijabla possibleChar 
    # Provjerava je li kontura unutar prediđenih granica
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and 
        possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False
# ----------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------------
#  Pozivanje funckije iz skripte DetectPlates
def findListOfListsOfMatchingChars(listOfPossibleChars):

    listOfListsOfMatchingChars = [] 

    
    # Već formirana lista i poznata varijabla konture, possibleChar
    for possibleChar in listOfPossibleChars: 
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)     # LOKALNA PROMJENA

        listOfMatchingChars.append(possibleChar)

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:
            continue

        # Stvaranje liste sa konturama koje se ponavljaju
        listOfListsOfMatchingChars.append(listOfMatchingChars)

        listOfPossibleCharsWithCurrentMatchesRemoved = []

        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)

        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)

        break

    # Vraća listulistaMogucih znakova
    return listOfListsOfMatchingChars
# -------------------------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#  DRUGA POZVANA FUNCKIJA
def findListOfMatchingChars(possibleChar, listOfChars):

    listOfMatchingChars = []

    for possibleMatchingChar in listOfChars:
        if possibleMatchingChar == possibleChar:    
                                                    
            continue                                
        
#-------------------------------------------  PROSTOR MEĐU ZNAKOVIMA   ----------------------------------------------------------------------------------------
        # Računa udaljenost između znakova
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)   #  LOKALNA PROMJENA

        # RAčuna kut između znakova
        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)     #  LOKALNA PROMJENA

        # Neke radnje
        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)
        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        #  Ukoliko su dimenzije između znakove dobre, znak se ubacuje na listu dobrih znakova
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):

            listOfMatchingChars.append(possibleMatchingChar)

    return listOfMatchingChars
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------  UDALJENOSTI IZMEĐU ZNAKOVA   ------------------------------
def distanceBetweenChars(firstChar, secondChar):

    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
#--------------------------------------------------------------------------------


# ------------------  KUTEVI IZMEĐU ZNAKOVA   ------------------------------------
def angleBetweenChars(firstChar, secondChar):

    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:
        fltAngleInRad = math.atan(fltOpp / fltAdj)
    else:
        fltAngleInRad = 1.5708 

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)

    return fltAngleInDeg
#----------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------------
# Iz skripte  main.py
# Sadržava listu mogucih tablica
def detectCharsInPlates(listOfPossiblePlates):

    # Brojač kontura oznake
    intPlateCounter = 0
    imgContours = None
    # Niz mogucih kontrura
    contours = []

    # SLucaj da je broj tablica 0, odmah gotova funkcija
    if len(listOfPossiblePlates) == 0:
        return listOfPossiblePlates 


    # FOR Petlja trazenje moguce tablice na listi tablica
    for possiblePlate in listOfPossiblePlates:


        # Pozivanje skirpte i funkcije    Preprocess
        possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate)
        # Obrada konture, šum i treshold

        # Obrade slike, moguce tablice
        possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.6, fy = 1.6)
        thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        #  Pozivanje lokalne funkcije    findPossibleCharsInPlate
        listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)
        # Vraća listu mogucih znakova

        # Pozivanje gornje lokalne funkcije   findListOfListsOfMatchingChars
        listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)
        # Vraća listulistaMogucih znakova


        if (len(listOfListsOfMatchingCharsInPlate) == 0):

            possiblePlate.strChars = ""
            continue

            # Proalzi kroz listu mogucih znakova
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)

            # Poziv donje lokalne funckije za brisanje preklapajucih znakova
            listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])  
            # Vrača   listOfMatchingCharsWithInnerCharRemoved      

        intLenOfLongestListOfChars = 0
        intIndexOfLongestListOfChars = 0

        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
                intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
                intIndexOfLongestListOfChars = i

        longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

        # Ide na Azure dio
        possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)

    return listOfPossiblePlates
# -----------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------------
# Poziva se iz gornje funkcije  detectCharsInPlates
def findPossibleCharsInPlate(imgGrayscale, imgThresh):

    listOfPossibleChars = []
    contours = []
    imgThreshCopy = imgThresh.copy()

    # Trazenje kontura na jedinoj mogucoj tablici
    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Pregladavenj svake konture je li znak
    # TO se obavlja zvanjem funkcije u skripti PossibleCHar
    for contour in contours:
        # Je li kontura znak
        possibleChar = PossibleChar.PossibleChar(contour)

        # Ukoliko je kontura stvarno znak dodaje su na listu mogucih znakova
        if checkIfPossibleChar(possibleChar):
            listOfPossibleChars.append(possibleChar)

    # Vraća listu mogucih znakova
    return listOfPossibleChars
#-----------------------------------------------------------------------------------------------------------------------------------------

    

# -----------------------------------------------------------------------------------------------------------------------------------------
# FUnckija pozvana gore za micanje preklapajucih znakova
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)

    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar: 
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)
                    else:
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)

    return listOfMatchingCharsWithInnerCharRemoved
# ---------------------------------------------------------------------------------------------------------------------------------------------



#   -------------------- PREPOZNAVANJE ZNAK PO ZNAK --------------------------------------------------------------------------------------------------

def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = "" 

    height, width = imgThresh.shape

    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)

    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)
    i=0
    j=1
    allChars=""

    # Ide kroz svaki znak točne tablice
    for currentChar in listOfMatchingChars:
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        cv2.rectangle(imgThreshColor, pt1, pt2, Main.SCALAR_GREEN, 2)

        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        # Slika se postavlja na širinu 15 a visinu 25
        imgROIResized = cv2.resize(imgROI, (15, 25))

        # Odlazi u skriptu Determination.py
        currentChar=det.RecognizeChar(imgROIResized)

        # Dodavanje znaka u konačni niz znakova
        allChars+=currentChar
        if(len(listOfMatchingChars)==7):
            if(j==2):
                allChars+=" "
            if(j==5):
                allChars+="-"
        elif(len(listOfMatchingChars)==8):
            if(j==2):
                allChars+=" "
            if(j==6):
                allChars+="-"
        i+=1
        j+=1

    # Ispisuje znakove u konzulu
    print("\n\n" + allChars)
    return strChars
# ------------------------------------------------------------------------------------------------------------------------------------------------------------








