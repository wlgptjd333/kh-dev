from ultralytics import YOLO


def main():
    model = YOLO('yolo26n.pt')



    model.train(
        data='dataset/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name="kh_detector",
    )

if __name__ == '__main__':
    main()

