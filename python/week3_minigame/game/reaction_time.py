# reaction_game.py

import tkinter as tk
import random
import time

# 전역 변수 선언
state = "READY"
start_time = 0
timer_id = None
label = None
window = None


def on_click(event):
    global state, start_time, timer_id, label, window

    if state == "READY":
        state = "WAITING"
        label.config(text="초록색이 되면 클릭하세요!", bg="red", fg="white")
        delay = random.randint(2000, 5000)
        timer_id = window.after(delay, show_green)

    elif state == "WAITING":
        state = "READY"
        if timer_id:
            window.after_cancel(timer_id)  # 예약해둔 초록불 켜기 취소!
        label.config(text="너무 빨리 눌렀습니다!\n다시 하려면 클릭하세요.", bg="blue", fg="white")

    elif state == "CLICK_NOW":
        end_time = time.time()
        reaction_time = (end_time - start_time) * 1000
        state = "READY"
        label.config(text=f"반응속도: {reaction_time:.0f} ms!\n다시 하려면 클릭하세요.", bg="white", fg="black")


def show_green():
    global state, start_time, label
    state = "CLICK_NOW"
    label.config(text="지금 클릭하세요!!!", bg="green", fg="white")
    start_time = time.time()


# 📌 main.py에서 reaction_time.play_reaction_time() 으로 호출할 함수!
def play_reaction_time():
    global window, label, state, timer_id, start_time

    # 게임 재실행 시 상태 초기화
    state = "READY"
    start_time = 0
    timer_id = None

    window = tk.Tk()
    window.title("반응속도 테스트")
    window.geometry("400x300")

    label = tk.Label(window, text="화면을 클릭하면 시작합니다.", font=("맑은 고딕", 16, "bold"), bg="white")
    label.pack(expand=True, fill="both")
    label.bind("<Button-1>", on_click)

    window.mainloop()


# 이 파일만 단독으로 실행해서 테스트해보고 싶을 때 사용
if __name__ == "__main__":
    play_reaction_time()