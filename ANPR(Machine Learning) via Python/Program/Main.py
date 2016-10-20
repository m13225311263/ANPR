import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate

SCALAR_GREEN = (0.0, 255.0, 0.0)


def main():

    imgOriginalScene  = cv2.imread("LicPlateImages/tablica7.png") 

    if imgOriginalScene is None:                            
        print ("\nerror: image not read from file \n\n")      
        os.system("pause")                                  
        return                                              

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0: 
        print ("\nno license plates were detected\n")
    else: 
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0]
 
        cv2.imshow("imgThresh", licPlate.imgThresh)
        
        cv2.imshow("imgOriginalScene", imgOriginalScene)

    cv2.waitKey(0)

    return

if __name__ == "__main__":
    main()
