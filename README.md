# Drowsiness Detection System

## Features

- **Image Detection**: Analyze single images or batches of images for drowsiness
- **Real-time Detection**: Live webcam feed analysis with alert system
- **Batch Processing**: Process entire datasets for evaluation
- **Configurable**: Easy-to-modify detection parameters and thresholds
- **Visualization**: Save images with detection boxes and confidence scores

## Project Structure

```
DrowsinessDetector/
├── src/
│   ├── __init__.py
│   ├── detector.py      # Main detection class
│   └── utils.py         # Utility functions
├── Driver Drowsiness Dataset (DDD)/
│   ├── Drowsy/          # Drowsy images
│   └── Non Drowsy/      # Non-drowsy images
├── config.py            # Configuration settings
├── main.py              # Main script with CLI
├── demo.py              # Real-time demo script
├── simple_inference_test.py  # Simple test script
├── requirements.txt     # Python dependencies
└── yolo11n.pt          # YOLO model fileconda remove --name
```

## Installation

1. **Clone or download the project**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
