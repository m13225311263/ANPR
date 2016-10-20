import urllib.request
import cv2
import json
import numpy as np

def getPrediction(char):

    cols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

    for i in range(0,15):
        number=0
        for j in range (0,25):
            if(char[j][i]<200):
                number+=1
        cols[i]=number
        
    im2, contours, hierarchy = cv2.findContours(char, 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt)
    if(M['m00']!=0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else:
        cx=0
        cy=0
       
    data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["klasa", "c1", "c2", "c3","c4", "c5", "c6","c7", "c8", "c9","c10", "c11", "c12","c13", "c14", "c15","cx", "cy"],
                        "Values": [ [ "C",cols[0], cols[1], cols[2],cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9], cols[10], cols[11], cols[12], cols[13], cols[14], cx, cy]]
                    },        },
                "GlobalParameters": {
    }
        }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/72d85169b22d4d548637997d8b94a5d0/services/194ce0186ec64d0bad247508e08e39fd/execute?api-version=2.0&details=true'
    api_key = 'GpwM+jt2xXnRwLkr8Nr5zqn+HC9NDk16l1Hfm5BPyvhZzNGF3peZZiz2cwUDss0ItfCUZXurJm3LVK8ci61tQQ=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)
    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        prediction= json.loads(result.decode())
        t1 = prediction['Results']
        t2 = t1['output1']
        t3 = t2['value']
        t4 = t3['Values']
        return t4[0][44] #Podesiti
        
    except urllib.request.HTTPError.error:
        print("The request failed with status code: " + str(error.code))
        return 5
