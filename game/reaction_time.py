# reaction_game.py

import tkinter as tk
import random
import time

state = "READY"       # 현재 상태: READY(준비), WAITING(빨간불 대기), CLICK_NOW(초록불)
start_time = 0        # 초록불이 켜진 시간을 기록
timer_id = None       # 너무 빨리 눌렀을 때 예약을 취소하기 위한 타이머 번호

def on_click(event):
    global state, start_time, timer_id

    # 1. 처음 클릭했을 때 (대기 시작)
    if state == "READY":
        state = "WAITING"
        label.config(text="초록색이 되면 클릭하세요!", bg="red", fg="white")
        
        # 2초(2000ms) ~ 5초(5000ms) 사이 랜덤한 시간 뒤에 초록불 켜기 예약
        delay = random.randint(2000, 5000)
        timer_id = window.after(delay, show_green)

    # 2. 초록불이 되기 전에 너무 빨리 클릭했을 때 (부정출발)
    elif state == "WAITING":
        state = "READY"
        window.after_cancel(timer_id) # 예약해둔 초록불 켜기 취소!
        label.config(text="너무 빨리 눌렀습니다!\n다시 하려면 클릭하세요.", bg="blue", fg="white")

    # 3. 초록불이 켜졌을 때 정상적으로 클릭했을 때 (반응속도 측정)
    elif state == "CLICK_NOW":
        end_time = time.time()
        # 끝난 시간 - 시작 시간 = 반응속도 (1000을 곱해서 밀리초(ms)로 변환)
        reaction_time = (end_time - start_time) * 1000 
        state = "READY"
        label.config(text=f"반응속도: {reaction_time:.0f} ms!\n다시 하려면 클릭하세요.", bg="white", fg="black")

def show_green():
    """시간이 다 되면 초록불로 바꾸는 함수"""
    global state, start_time
    state = "CLICK_NOW"
    label.config(text="지금 클릭하세요!!!", bg="green", fg="white")
    start_time = time.time() # 초록불이 켜진 바로 이 순간의 시간을 기록!

# GUI
window = tk.Tk()
window.title("반응속도 테스트")
window.geometry("400x300")

# 라벨 만들기
label = tk.Label(window, text="화면을 클릭하면 시작합니다.", font=("맑은 고딕", 16, "bold"), bg="white")
label.pack(expand=True, fill="both") # 창 전체를 채우도록 확장

# 마우스 왼쪽 버튼 온 클릭 함수 연결
label.bind("<Button-1>", on_click)

# 창이 꺼지지 않고 계속 떠있게 무한 반복
window.mainloop()