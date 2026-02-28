def power(n):
    for i in range(1,n+1):
        yield i*i
for i in power(5):
    print(i)