from ultralytics import YOLO

model = YOLO("best.pt")

results = model("test_images",
                save=True,
                conf=0.5,
                exist_ok=True,
                project="/dev/dl/prj06/projecttttt",
                name="nameeeee",
                )
print(len(results))