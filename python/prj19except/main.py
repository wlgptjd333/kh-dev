# 예외 처리

try:
    x = int(input("x : "))
    y = int(input("y : "))
    result = x / y
    print(result)
except Exception as e:
    print(e)
    print(type(e))
else:
    print("Great!")
finally:
    print("Goodbye")

print("finish ~~~~~")