from datetime import date, timedelta

t = date.today()
f = t - timedelta(days=5)
print("Бүгін:", t)
print("Бес күн бұрын:", f)
