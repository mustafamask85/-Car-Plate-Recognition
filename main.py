import cv2 
import pandas as pd
from paddleocr import PaddleOCR
from ultralytics import YOLO
import numpy as np
import cvzone 
import os
from server import manage_number_platte


os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
model = YOLO("car_platte_12s.pt")

ocr = PaddleOCR()


#cap = cv2.VideoCapture(0) # this is read from camera
cap = cv2.VideoCapture('nrc.mp4') # this is read from video 

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video_writer = cv2.VideoWriter("test.mp4",fourcc,30,(1020,500)) # this to save the output video 





area = [(124,339) , (127,451) , (485,440) , (460,328)] # this is the region of intrest 
counter = []

def perform_ocr(image_array): # this is function of ocr  (extract text from images)
    if image_array is None:
        raise ValueError(" Image is None")
    
    results = ocr.ocr(image_array , rec = True)
    
    detected_text = []
    if results[0] is not None:
        #print(results)
        for result in results[0]:
            text = result[1][0]
            detected_text.append(text)

        return '' .join(detected_text)    
    

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame , (1020,500)) #to resize  frame
    # cv2.polylines(frame,[np.array(area,np.int32)],True,(0,255,0),2)
    results = model.track(frame,persist=True) # passing the frame to our model to detect
    
    if results[0].boxes is not None and results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for box,class_id,track_id in zip(boxes,class_ids,track_ids):
    
            x1,y1,x2,y2 = box
            cx = int(x1+x2)//2
            cy = int(y1+y2)//2
       
        result = cv2.pointPolygonTest(np.array(area , np.int32) , ((cx,cy)) , False)   #this is for detect in specfic region 
        if result >= 0:

            cv2.rectangle(frame , (x1,y1), (x2,y2) , (97,233,12) , 2) # this is to draw the rectangle 
            
            if track_id not in counter:
                counter.append(track_id)
                # cv2.rectangle(frame , (x1,y1), (x2,y2) , (97,233,12) , 2) # this is to draw the rectangle 
                crop = frame[y1:y2 , x1:x2]
                crop = cv2.resize(crop , (110,30))
                text = perform_ocr(crop)
                text = text.replace('(', '').replace(')', '').replace(',', '').replace(']', '').replace('-', ' ')
                cvzone.putTextRect(frame , f'{text}' , (cx-50 , cy-30) , 1 ,2,colorR=(117,37,12))
                manage_number_platte(text)
    #video_writer.write(frame) # this is to save output video
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()
#video_writer.release()
 