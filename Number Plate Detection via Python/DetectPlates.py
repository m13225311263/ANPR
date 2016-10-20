
# ---------------------------------- UKLJUČIVANJE MODULA -------------------------
import cv2
import numpy as np
import math
import random
# -------------------------------------------------------------------------------


# -------------------------------- UKLJUČIVANJE VANJSKIH SKRIPTI --------------
import Main
import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar
# -------------------------------------------------------------------------------


PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5


# -------------------------------------------------------------------------------------------------------------------------------------------
#  Poziv iz Main.py skripte
def detectPlatesInScene(imgOriginalScene):

    # Niz sa potencijalnim tablicama, isti kao u Main.py
    listOfPossiblePlates = []

    # Ddređivanje visine, širine i broja kanala originalne slike
    height, width, numChannels = imgOriginalScene.shape
    # Prazne matrice u koje se sprema obrađena slika. 
    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)
    # Uništavanje prozora
    cv2.destroyAllWindows()

    # -----------------------------    PREOBRADA SLIKE - PREPROCESS  ( 1 ) --------------------------------------------------

    # Pozivanje druge skripte i istoimene funkcije u njoj Preprocess
    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)                 # PROMJENA      Preprocess.py
    # Vraćanje iz Preprocess skripte sa dvije matrice, imgGrayscale i imgTresh
    
    # ------------------------------------------------------------------------------------------------------------------


    # -----------------------------       TRAŽENJE ZNAKOVA   ( 2 )  -------------------------------------------------------------

    # Funkcija koristi matricu   imgTreshScene ( crno-bijela slika bez šuma ) - binarna slika
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)                                 # LOKALNA PROMJENA
    # Dobivene su konture koju su najvjerojantije znak, jer su mjerene dimenzije

    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)     # PROMEJNA
    # Vraća listulistaMogucih znakova 


    #  Traženje tablice medju mogucim tablicama
    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)   # LOKALNA PROMJENA
        # Došla possible plate iz funcije extract plate

        # Ukoliko tablica postoji, dodajes se u listu tablica
        if possiblePlate.imgPlate is not None: 
            listOfPossiblePlates.append(possiblePlate)

    # Ispis na konzoli : broj pronađenih tablica
    print ("\n" + str(len(listOfPossiblePlates)) + " possible plates found")

    # Vraća broj mogucih tablica
    return listOfPossiblePlates

# -------------------------------------------------------------------------------------------------------------------------------------------------------------







#--------------------------------------------------------------------------------------------------------------------------------------
# FUnckija za traženje znakova na slici
def findPossibleCharsInScene(imgThresh):

    # Matrica koja očekuje moguće znakove
    listOfPossibleChars = []
    # Varijabla koja broji potencijalne znakove
    intCountOfPossibleChars = 0  

    # Kopija matrice imgTresh sa tresholdanom slikom
    imgThreshCopy = imgThresh.copy()


    # --------------------------------------------   KONTURE   --------------------------------------------------------------------
    # CV funkcija
    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Određivanje visine i širine slike
    height, width = imgThresh.shape
    # Prazna matrica 
    imgContours = np.zeros((height, width, 3), np.uint8)


    # FOR petlja koja prolazi kroz sve moguce kontura
    # Broj kontura definiran ranije korištenjem CV funckije findContours
    for i in range(0, len(contours)):

        # Šalje svaku konturu na pregled, je li možda znak
        possibleChar = PossibleChar.PossibleChar(contours[i])           #  PROMJENA
        # Dobije se veličina, OMJER konture    (podaci o konturi)


        # Pozivanje funckije checkIfPossibleChar iz skripte DetectChars, kojoj predajem varijablu possibleChar
        if DetectChars.checkIfPossibleChar(possibleChar):    #   PROMJENA
        #  GLeda je li kontura dovoljne, definirane veličine koja je znak 

            #  DOBRA KONTURA - MOGUCI ZNAK
            # Ukoliko je kontora dobra, povećava se gore navedena varijbal koja broji moguce znakove
            intCountOfPossibleChars = intCountOfPossibleChars + 1
            # Untar gore deklariranog niza, appenda se kontura, odnosno moguci znak .....DA
            listOfPossibleChars.append(possibleChar)

    # Lista kontura koji su moguci znakovi
    return listOfPossibleChars
# ---------------------------------------------------------------------------------------------------------------------------------------------------





#----------------------------------------------------    DOBIVANJE PRAVE TABLICE     -----------------------------------------------------------------------
#   LOKALNA FUNCKIJA
#   Traženje tablice nakon što se dobila  listOfMatchingChars
def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)

    # Određivanje centra  tablice, prvi i zadnji znak
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    # Kordinate centra tablice
    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    # Širina tablice
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape 

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possiblePlate.imgPlate = imgCropped

    # Vraća mogucu tablicu !!! 99% jednu jedinu!!!
    return possiblePlate
#-------------------------------------------------------------------------------------------------------------------------------------------------------











