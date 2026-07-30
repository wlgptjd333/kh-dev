import copy
import random

from model.pikachu import Pikachu
from model.lizard import Lizard
from model.turtle import Turtle


def battle(attacker, defender):
    print(f"\"{attacker.name}\"는 \"{defender.name}\"에게 공격!")
    defender.hp -= attacker.atk
    print("공격한 포켓몬: ", attacker)
    print("맞은 포켓몬: ", defender)


p1 = Pikachu()
p2 = Lizard()
p3 = Turtle()

p_list = [p1, p2, p3]

# 포켓몬 목록 출력
print("----- pokemon list -----")
print(1, p1)
print(2, p2)
print(3, p3)
print()

# 유저 포켓몬 출력
num = int(input("원하는 포켓몬 번호: ")) - 1
user = copy.deepcopy(p_list[num])

num = random.randint(1, len(p_list)) - 1
com = copy.deepcopy(p_list[num])

# 배틀 실행
while True:
    # 유저가 공격
    battle(user, com)
    if com.hp <= 0:
        break

    # 컴퓨터가 공격
    battle(com, user)
    if user.hp <= 0:
        break
