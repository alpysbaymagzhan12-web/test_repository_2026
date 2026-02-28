def sq(a, b):
    for i in range(a, b+1):
        yield i * i

for j in sq(3, 7):
    print(j)
