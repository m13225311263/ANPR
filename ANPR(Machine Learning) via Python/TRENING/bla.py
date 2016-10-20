import cv2
import numpy as np
import os


def GetTrainingCSV():
    names=["2a.jpg","2c.jpg"]#,"7.jpg"]#,"7b.jpg"]#,"012.jpg","013.jpg",]
    with open("training.csv","w+") as f:
        f.write("klasa,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,cx,cy\n")
        for i in range(len(names)):
            img=cv2.imread(names[i],0)
            f.write('U,')
            for j in range(0,15):
                number=0
                for k in range (0,25):
                    if(img[k][j]<200):
                        number+=1
                if(k!=14):
                    f.write(str(number)+",")
                else:
                    f.write(str(number))
            im2,contours,hierarchy = cv2.findContours(img, 1, 2)
            cnt = contours[0]
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            perimeter=cv2.arcLength(cnt,True)
            f.write('{0},{1}\n'.format(cx,cy))

GetTrainingCSV()

