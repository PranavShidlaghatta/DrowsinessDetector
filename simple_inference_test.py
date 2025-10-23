import os
import random
from ultralytics import YOLO

# Load YOLOv11n model
model = YOLO('yolo11n.pt')

# Dataset paths
base_dir = 'Driver Drowsiness Dataset (DDD)'
drowsy_dir = os.path.join(base_dir, 'Drowsy')
non_drowsy_dir = os.path.join(base_dir, 'Non Drowsy')

# Get image files
drowsy_images = [f for f in os.listdir(drowsy_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
non_drowsy_images = [f for f in os.listdir(non_drowsy_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Found {len(drowsy_images)} drowsy images and {len(non_drowsy_images)} non-drowsy images")

# Test on a few sample images
sample_images = (
    [os.path.join(drowsy_dir, img) for img in drowsy_images[:3]] +
    [os.path.join(non_drowsy_dir, img) for img in non_drowsy_images[:3]]
)

# Run inference
for img_path in sample_images:
    print(f"\nProcessing: {os.path.basename(img_path)}")
    results = model(img_path)
    results[0].show()  # Display image with detections

    # Print detection info
    if results[0].boxes is not None:
        for box in results[0].boxes:
            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = model.names[class_id]
            print(f"Detected: {class_name} (confidence: {confidence:.3f})")
    else:
        print("No detections found")
