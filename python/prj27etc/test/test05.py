# zip
from idlelib import history

names = ["홍길동", "임꺽정", "김철수"]
scores = [100, 200, 300]
height = [170,180,190]

zipped = zip(names, scores, height)
for n,s,h in zipped:
    print(n,s,h)