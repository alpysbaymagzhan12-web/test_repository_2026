# *args мысалы (кез келген санды қосу)
def sum_all(*numbers):
    total = sum(numbers)
    return total

print(sum_all(1, 2, 3, 4, 5)) # 15

# **kwargs мысалы (мәліметтер жинау)
def user_profile(**data):
    for key, value in data.items():
        print(f"{key}: {value}")

user_profile(aty="Марат", tegi="Ержанов", qalasy="Алматы")
