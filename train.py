from ultralytics import YOLO
import torch
import multiprocessing


def main():
   
    
    model = YOLO("yolov8m.pt")

    model.train(
    data="data.yaml",
    epochs=80,
    imgsz=640,
    batch=8,
    device=0,
    optimizer="AdamW",
    lr0=0.001,
    cos_lr=True,

    mosaic=0.5,
    mixup=0.0,
    hsv_h=0.01,
    hsv_s=0.5,
    hsv_v=0.3,
    degrees=2.0,
    translate=0.05,
    scale=0.3,
    shear=0.0,
    fliplr=0.5,

    close_mosaic=10,
    patience=20
)


if __name__ == "__main__":
    multiprocessing.freeze_support()   
    main()