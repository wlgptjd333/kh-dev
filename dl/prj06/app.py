import io
from pathlib import Path

from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO

x = Path(__file__).resolve().parent
model = YOLO("best.pt")

app = FastAPI()


# url : hello
# method : post (form)
# data : title
@app.post("/hello/{num}")
def test():
    print("test called~")
    results = model("test_images",
                    save=True,
                    conf=0.5,
                    exist_ok=True,
                    project=f"{x}/api_prj",
                    name="inf",
                    )


@app.post("/upload")
def upload(f: UploadFile = File()):
    if f.content_type not in ("image/jpeg", "image/jpg"):
        raise HTTPException(status_code=400, detail="Not allowed")
    print("upload called~")
    print(f.filename)
    print(f.content_type)
    data = f.file.read()
    # print(data)
    print(type(data))
    print(len(data))

    try:
        buffer = io.BytesIO(data)
        img = Image.open(buffer)
        img.convert("RGB")
    except:

        raise HTTPException(status_code=400, detail="can not read image")

    print(img)
    img.save("temp.jpg")

    return {
        "filename": f.filename,
        "content-type": f.content_type,
        "bytes": len(data),
        "width": img.width,
        "height": img.height,
    }


class Detection(BaseModel):
    cls_id: int
    cls_name: str
    conf: float
    bbox: list[float]


class PredictResponse(BaseModel):
    width: int
    height: int
    count: int
    detection_list: list[Detection]


@app.post("/predict/json")
def predict_json(f: UploadFile = File()) -> PredictResponse:
    data = f.file.read()
    buffer = io.BytesIO(data)
    img = Image.open(buffer)
    img = img.convert("RGB")
    results = model(img, conf=0.5, verbose=False)
    result = results[0]

    detection_list = []
    a = result.boxes.cls.tolist()
    b = result.boxes.conf.tolist()
    c = result.boxes.xyxy.tolist()
    for cls, conf, box in zip(a, b, c):
        d = Detection(
            cls_id=int(cls),
            cls_name=result.names[int(cls)],
            conf=round(conf, 3),
            bbox=[round(temp, 2) for temp in box],
        )
        detection_list.append(d)

    return PredictResponse(
        width=img.width,
        height=img.height,
        count=len(detection_list),
        detection_list=detection_list,
    )