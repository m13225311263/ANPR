# ---------------------------------- UKLJUČIVANJE MODULA ------------------------
import cv2   
import numpy as np
import os
# -------------------------------------------------------------------------------

# -------------------------------- UKLJUČIVANJE VANJSKIH SKRIPTI ----------------
import DetectPlates
import DetectChars      
import PossiblePlate  
# -------------------------------------------------------------------------------

SCALAR_GREEN = (0.0, 255.0, 0.0)

# --------------------------------- MAIN funkcija   -------------------------------------------------------------------------------
def main():

    #------------------------------UČITAVANJE SLIKE -------------------------------------------------------------------------------
    # Čitanje slike iz direktorije LicPlateImages
    imgOriginalScene  = cv2.imread("Tablice/tablica2.png")  
    # U slučaja nemogućnosti čitanja datoteke (slike)
    if imgOriginalScene is None:                            
        print ("\nERROR: image not read from file \n\n")      
        os.system("pause")                                  
        return                                              
    #----------------------------------------------------------------------------------------------------------------------------


    # --------------------------  TRAŽENJE TABLICA  ------------------------------------------------------------------------------- 

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)                      # PROMJENA   DetectPlates.py

    #------------------------------------------------------------------------------------------------------------------------------


    # -------------------------- TRAŽENJE ZNAKOVA ---------------------------------------------------------------------------------

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)                    # PROMJENA  DetectChars.py

    #-------------------------------------------------------------------------------------------------------------------------------


    #----------------------------------------- ISPIS I PRIKAZ TABLICE  --------------------------------------------------------------
    if len(listOfPossiblePlates) == 0: 
        print ("\nNo license plates were detected\n")
    else: 
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0]
        #  Prikaz slika
        cv2.imshow("imgThresh", licPlate.imgThresh)
        cv2.imshow("imgOriginalScene", imgOriginalScene)
    cv2.waitKey(0)
    return
    #-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------

# ------    Poziv MAIN funkcije  -----------------
if __name__ == "__main__":
    main()
# ------------------------------------------------

















