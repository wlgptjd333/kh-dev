from ultralytics import YOLO

model = YOLO('best.pt')
results = model('test_images', conf = 0.732, save=True)

for r in results:
    print(r.to_json())