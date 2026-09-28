from pathlib import Path
from ultralytics import YOLO

x = Path(__file__).resolve().parent

model = YOLO("best.pt")
results = model("test_images",
                save=True,
                conf=0.5,
                exist_ok=True,
                project=f"{x}/ppppp",
                name="nameeeee",
                )

print(len(results))