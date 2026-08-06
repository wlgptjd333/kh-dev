# thread
import threading
import time


for i in range(10):
    print("kh")
    time.sleep(0.1)

def f01():
    for i in range(10):
        print("hello")
        time.sleep(0.1)
def f02():
    for i in range(10):
        print("world")
        time.sleep(0.1)

t1 = threading.Thread(target=f01)
t2 = threading.Thread(target=f02)

t1.start()
t2.start()

print("end ~~~")