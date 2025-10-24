# docker_training.ps1
# custom run command example: .\docker_training.ps1 -Model yolov8n.pt -Epochs 50 -ImgSz 640 -Batch 8 -RunName drowsy_run2
param(
  [string]$Model   = "yolov8n.pt",
  [int]   $Epochs  = 100,
  [int]   $ImgSz   = 1280,
  [int]   $Batch   = 32,
  [string]$RunName = "drowsy_run1"
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path "$PWD\runs" | Out-Null

docker run --rm -it --gpus all `
  --shm-size=8g `
  --mount type=bind,src=${PWD}\data,dst=/workspace/data `
  --mount type=bind,src=${PWD}\runs,dst=/workspace/runs `
  ultralytics/ultralytics:latest `
  yolo detect train `
    data=/workspace/data/data.yaml `
    model=$Model `
    epochs=$Epochs imgsz=$ImgSz batch=$Batch workers=0 device=0 `
    project=/workspace/runs name=$RunName
