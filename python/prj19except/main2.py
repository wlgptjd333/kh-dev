from dog import Dog
age = int(input("What is your age? "))
if age < 0:
    print("Sorry, your age cannot be negative.")
    raise Dog("나이 음수 ㄴㄴ")
print(age)