'''
NOTE: 
- The python script that will run on the raspberry pi. 
'''

import cv2
from ultralytics import YOLO
from collections import deque

model = YOLO(r"/home/rayan/436/DrowsinessDetector/runs/drowsy_run5/weights/best.pt")
class_names = model.names  
# print(class_names)

window_size = 60 # around 2-4 seconds at 30 FPS
threshold = 0.3 # 30% of frames indicating drowsiness 

# Drowsy buffer will store last N frames at a time 
drowsy_buffer = deque(maxlen=window_size)

# NOTE: Pain point on linux dev, might be a failure point on pi OS. 
cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model.predict(frame, conf=0.25, verbose=False)
    annotated_frame = results[0].plot() 

    if results[0].boxes: 
        # for box in results[0].boxes:
        #     cls_idx = int(box.cls[0])      
        #     cls_name = class_names[cls_idx]
        #     conf = float(box.conf[0])  
        #     print(f"Detected class -->{cls_name}<-- with confidence {conf:.2f}")

        cls_idx = int(results[0].boxes[0].cls[0]) 
        if cls_idx in [1,2]:
            drowsy_signal = 1 
        else: 
            drowsy_signal = 0 
    else:
        drowsy_signal = 0
        # print("No detections")
    
    drowsy_buffer.append(drowsy_signal)
    
    drowsy_ratio = sum(drowsy_buffer) / len(drowsy_buffer)

    if drowsy_ratio > threshold:
        print("Drowsiness detected! 🚨")
    else: 
        print("Waiting...")

    cv2.imshow("Drowsiness Detector", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
