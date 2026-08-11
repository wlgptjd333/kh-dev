import json

# 1. 서버에서 날아온 json 데이터 (겉보기엔 딕셔너리 같지만 '문자열'입니다)
server_data = """
{
    "player_id": "Hye-sung",
    "game": "Valorant",
    "tier": "Ascendant",
    "stats": {
        "kills": 142,
        "deaths": 108,
        "headshot_rate": 35.5
    },
    "is_online": true
}
"""

# 2. 언패킹(Unpacking): 문자열을 파이썬 '딕셔너리'로 변환 (loads)
player_dict = json.loads(server_data)

print("--- 특정 데이터만 쏙 뽑아내기 ---")
print("접속자:", player_dict["player_id"])
print("헤드샷 비율:", player_dict["stats"]["headshot_rate"])

# 3. 파이썬 안에서 데이터 수정하기 (킬 수 증가, 로그아웃 처리)
player_dict["stats"]["kills"] += 1
player_dict["stats"]["deaths"] += 1

# 4. 패킹
print("---다시 포장하기---")
new_json_data = json.dumps(player_dict)
print(new_json_data)