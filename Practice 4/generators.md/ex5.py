def count(n):
    while n >= 0:
        yield n
        n -= 1


for n in count(5):
    print(n)
