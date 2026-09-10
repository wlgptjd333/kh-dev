import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 9876))
server_socket.listen()
print("나 서버소켓인데,,, 연결 대기중이야 ...")

clients = []


def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except Exception as e:
                print("[ERROR] broadcast", e)


def handle_client(conn, addr):
    print(f"{addr} 접속")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("not data : ", data)
                print("상대방 나감")
                break
            print("[상대방]", data.decode())
            broadcast(data, conn)
        except Exception as e:
            print("예외발생 !!!", e)
            break
    if conn in clients:
        clients.remove(conn)
    conn.close()


while True:
    conn, addr = server_socket.accept()
    print("접속한 addr : ", addr)
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()