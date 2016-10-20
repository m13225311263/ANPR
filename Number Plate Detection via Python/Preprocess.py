
# ---------------------------------- UKLJUČIVANJE MODULA -------------------------
import cv2
import numpy as np
import math
# -------------------------------------------------------------------------------

GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Pozvana od strane skripte DetectPlates
def preprocess(imgOriginal):

    # Pretvorba iz RGB u HSV format zbog boljeg kontrasta
    imgGrayscale = extractValue(imgOriginal)                                            # LOKALNA PROMJENA
    
    # Povećanje kontrasta na slici, koristi se varijabla imgGrayscale, tek nastala
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)                            # LOKALNA PROMJENA
    
    # Određivanje visine i širine slike
    height, width = imgGrayscale.shape

    # Prazna matrica
    imgBlurred = np.zeros((height, width, 1), np.uint8)

    # Uporaba GaussianBlur za otklanjanje šuma
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    
    # Uporaba Threshold-a
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    
    return imgGrayscale, imgThresh
#----------------------------------------------------------------------------------------------------------------------------------------------------------------



#----------------          PRETVORBA   RGB  u  HSV   --------------------------------------------
def extractValue(imgOriginal):
    # Određivanje visine i širine slike
    height, width, numChannels = imgOriginal.shape

    # Prazna matrica
    imgHSV = np.zeros((height, width, 3), np.uint8)

    # CV funkcije
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
#---------------------------------------------------------------------------------------------------



#------------------------ -----    POVEĆANJE KONTRASTA   ----------------------------------------------------
def maximizeContrast(imgGrayscale):
    # Određivanje visine i širine slike
    height, width = imgGrayscale.shape

    # Prazne matrice
    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    # CV funkcije
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)
    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
#--------------------------------------------------------------------------------------------------------------










