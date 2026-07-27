def student():
    score_dict = {"김철수": {"국어": 100, "영어": 70}, "홍길동": {"국어":10, "영어": 50}}
    return score_dict


print(student())
print(student()["김철수"])
print(f"{student().keys()}")
print(student())

std_list = [
    {"name": "hone", "score": 100} ,
    {"name": "kim", "score": 200} ,
    {"name": "lee", "score": 300} ,
]

for std_info in std_list:
    print(f"{std_info["name"]} 학생의 성적은 {std_info["score"]} 입니다")