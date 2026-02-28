from datetime import date, timedelta

a = date.today()
b = a - timedelta(days=1)
c = a + timedelta(days=1)

print("Кеше:", b)
print("Бүгін:", a)
print("Ертең:", c)
