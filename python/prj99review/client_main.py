import socket
import threading

# 클라이언트 소켓 생성 및 서버 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.40.97", 9876))

nickname = input("nickname: ")

# 스레드용 수신 함수
def receive():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("not data : ", data)
                print("상대방 나감")
                break
            print("[상대방]", data.decode())
        except Exception as e:
            print("예외발생 !!!", e)
            break

threading.Thread(target=receive,daemon=True).start()

while True:
    # 발신
    msg = input("보낼 메시지 : ")
    msg = f"\n[{nickname}]: {msg}"
    client_socket.send(msg.encode())