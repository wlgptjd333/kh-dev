# 쓰레드
import threading

def hello(nickname:str="guest"):
    print(f"Hello {nickname} !")

t1 = threading.Thread(target=hello, args=("guest",))
t1.start()
