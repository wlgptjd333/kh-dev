def x():
    print("x")
    return y

y = x

def f01():
    print("f01")
    return x

f02 = f01()
f01()
f02()
result = f02()
result()

# class, instance, attribute, method
# 상속
print(100)
print(100)
print(10,20,30,40,50,60,70)
print(10,20,30,40,50,60)