
# ---------------------------------- UKLJUČIVANJE MODULA -------------------------
import cv2
import json
import numpy as np
# -------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------------------
def RecognizeChar(char):

    cols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

    # Prolazi kroz matricu ( sliku znaka) i gleda je li vrijednost manja od 200 i računa vrijednost svakog stupca oznake JEDNOG ZNAKA
    stupac=0
    sredina=0
    for i in range(0,15):
        number=0

        for j in range (0,25):
            if(char[j][i]<200):  
                number+=1    
            if(char[i][12]>200): # Vrijednost 12. retka 
                sredina+=1
        cols[i]=number  
    stupac+=cols[i]
  
    #print(stupac)
    #print(sredina)



    for i in range(0,15):
        if((cols[i]>50)and(cols[i]<55)):
            char="A"
        elif((cols[i]>11) and (cols[i]<13) and (sredina>349) and (sredina<351)):
            char="B"
        elif((cols[i]>21) and (cols[i]<25) and (sredina>124) and (sredina<126)):
            char="C"
        elif((cols[i]>4) and (cols[i]<6) and (sredina>349) and (sredina<351)):
            char="D"
        elif((cols[i]>20) and(cols[i]<25) and (sredina>74) and (sredina<101)):
            char="E"
        elif((cols[i]>23) and (cols[i]<25) and (sredina>74) and (sredina<101)):
            char="F"
        elif((cols[i]>22) and (cols[i]<24) and (sredina>174) and (sredina<176)):
            char="G"
        elif((cols[i]>85) and (cols[i]<90)):
            char="H"
        elif((cols[i]>90) and (cols[i]<95)):
            char="I"
        elif((cols[i]>4) and (cols[i]<6) and (sredina>374) and (sredina<376)):
            char="J"
        elif((cols[i]>18) and (cols[i]<25) and (sredina>24) and (sredina<126)):
            char="K"
        elif((cols[i]>105) and (cols[i]<110)):
            char="L"
        elif((cols[i]>110) and (cols[i]<115)):
            char="M"
        elif((cols[i]>10) and (cols[i]<12) and (sredina>324) and (sredina<326)):
            char="N"
        elif((cols[i]>8)and (cols[i]<11) and (sredina>324) and (sredina<326)):
            char="O"
        elif((cols[i]>13) and(cols[i]<15) and (sredina>224) and (sredina<326)):
            char="P"
        elif((cols[i]>24) and (cols[i]<26) and (sredina>249) and (sredina<251)):
            char="R"
        elif((cols[i]>23) and (cols[i]<25) and (sredina>274) and (sredina<276)):
            char="S"
        elif((cols[i]>21) and (cols[i]<23) and (sredina>74) and (sredina<76)):
            char="T"
        elif((cols[i]>5) and (cols[i]<7) and (sredina>374) and (sredina<376)):
            char="U"
        elif((cols[i]>18) and(cols[i]<20)):
            char="V"
        elif((cols[i]>155)and (cols[i]<160)):
            char="Z"
        elif((cols[i]>21)and (cols[i]<23)):
            char="1"
        elif((cols[i]>17) and (cols[i]<20) and (sredina>249) and (sredina<375)):
            char="2"
        elif((cols[i]>18) and (cols[i]<22) and (sredina>299) and (sredina<326)):
            char="3"
        elif((cols[i]>2)and (cols[i]<4) and (sredina>349) and (sredina<376)):
            char="4"
        elif((cols[i]>12) and (cols[i]<19) and (sredina>249) and (sredina<251)):
            char="5"
        elif((cols[i]>22) and (cols[i]<26) and (sredina>149) and (sredina<201)):
            char="6"
        elif((cols[i]>190) and (cols[i]<195)):
            char="7"
        elif((cols[i]>193) and (cols[i]<197)):
            char="8"
        elif((cols[i]>7) and (cols[i]<16) and (sredina>324) and (sredina<351)):
            char="9"
        else: 
            char="0"
    return char
# -----------------------------------------------------------------------------------------------------------------------------------------------------
    
       
        
        



       
    

    
 