'''
NOTE: 
- The python script that will run on the raspberry pi. 
--> May need to package in a docker container with ARM .whl installations. 
--> I see the camera device module becoming a problem in time.
'''

import cv2
from ultralytics import YOLO
import requests
from collections import deque
import time 

# NOTE: ORIGINALLY USED DROWSY_RUN5/WEIGHTS/BEST.PT
model = YOLO(r"/home/rayan/436/DrowsinessDetector/runs/drowsy_run5/weights/best.pt")
class_names = model.names  
FASTAPI_URL = "http://localhost:8000/piRunner"
# print(class_names)
# { 0: No Yawn , 1: Yawn , 2: closed eyes , 3: open eyes }

window_seconds = 5 # original 2 seconds 
threshold = 0.3 # 30% of frames indicating drowsiness 
alpha = 0.95 # original 0.9 
momentum_score = 0  
drowsy_buffer = deque()

# Exponential weighted moving average 
# def ewma_momentum(drowsy_buffer, alpha=0.9, momentum_score = 0):
#     weighted_sum = 0 
#     weight_total = 0
#     N = len(drowsy_buffer)
#     for i, (ts, signal) in enumerate(drowsy_buffer):
#         weight = alpha ** (N - i - 1)
#         weighted_sum += signal * weight 
#         weight_total += weight 
#     weighted_ratio = weighted_sum / weight_total if weight_total != 0 else 0 

#     momentum_score = alpha * momentum_score + (1 - alpha) * weighted_ratio

#     return momentum_score

def rolling_average(drowsy_buffer, alpha=0.95, prev_score=0):
    if not drowsy_buffer:
        return 0
    # Compute average of signals in buffer
    avg_signal = sum(signal for _, signal in drowsy_buffer) / len(drowsy_buffer)
    # Optional smoothing
    smoothed = alpha * prev_score + (1 - alpha) * avg_signal
    smoothed = avg_signal
    return smoothed


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

    # originally 0.25
    results = model.predict(frame, conf=0.485, verbose=False)
    annotated_frame = results[0].plot() 

    if results[0].boxes: 
        # for box in results[0].boxes:
        #     cls_idx = int(box.cls[0])      
        #     cls_name = class_names[cls_idx]
        #     conf = float(box.conf[0])  
        #     print(f"Detected class -->{cls_name}<-- with confidence {conf:.2f}")

        cls_idx = int(results[0].boxes[0].cls[0]) 
        drowsy_signal = 1 if cls_idx in [1,2] else 0 
    else:
        drowsy_signal = 0
        # print("No detections")

    curr_time = time.time()
    drowsy_buffer.append((curr_time, drowsy_signal))

    # only hold frames that are within sliding window of `window_seconds` length 
    while drowsy_buffer and (curr_time - drowsy_buffer[0][0]) > window_seconds: 
        drowsy_buffer.popleft()
    
    # drowsy_ratio = sum(signal for (ts, signal) in drowsy_buffer) / len(drowsy_buffer)
    momentum_score = rolling_average(drowsy_buffer, alpha, momentum_score)

    try: 
        payload = {"drowsiness_score": float(momentum_score)}
        requests.post(FASTAPI_URL, json=payload, timeout=0.5)
    except requests.exceptions.RequestException as e: 
        print(f"Failed to send score {e}")

    if momentum_score > threshold:
        print("Drowsiness detected! 🚨")
    else: 
        print("Waiting...")

    cv2.imshow("Drowsiness Detector", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
