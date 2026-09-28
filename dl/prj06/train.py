from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO('yolo26n')
    model.train(
        data="dataset/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        name="train_result",
    )