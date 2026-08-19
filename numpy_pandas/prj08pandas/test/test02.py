import pandas as pd

employees = pd.read_csv("data/employees.csv")
orders = pd.read_csv("data/orders.csv")
departments = pd.read_csv("data/departments.csv")
customers = pd.read_csv("data/customers.csv")
city_grade = pd.read_csv("data/city_grade.csv")

# 1-1
print(employees.head())
# 1-2
print(employees.shape)
# 1-3
print(employees.info())
# 1-4
print(employees[["나이", "연봉"]].describe())
# 1-5
print(employees["부서코드"].value_counts())
# 1-6
print(orders["카테고리"].value_counts())
#