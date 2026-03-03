from ultralytics import YOLO
import multiprocessing

def main():
    model = YOLO("runs/detect/train/weights/best.pt")
    model.train(
        data="dataset/data.yaml",
        epochs=25,
        imgsz=512,
        batch=4,
        lr0=0.0003,
        multi_scale=False,
        close_mosaic=10,
        patience=10,
        device=0,
        workers=0,
        cache=False,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=10,
        translate=0.1,
        scale=0.5,
        fliplr=0.5
    )

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()