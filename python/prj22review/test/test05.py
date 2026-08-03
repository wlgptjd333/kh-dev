# try ~ except ~ else ~ finally
# raise

# try:
#     pass # 예외 발생 시
# except 예외타입 | 예외타입 as x:
#     pass # try 블럭 내 예외타입 일치하면? 잡아서 처리함
# except 예외타입 as x:
#     pass # except 여러개 가능 (단, 위쪽 코드부터 실행되므로 아래쪽으로 내려갈수록 넓은 범위로 설정)
# else:
#     pass # 예외 발생 없으면 실행되는 블럭
# finally:
#     pass # 무조건 실행 (예외 발생 여부 무관, return 이 있어도 동작함)