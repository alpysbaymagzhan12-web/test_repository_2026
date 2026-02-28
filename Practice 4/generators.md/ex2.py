def even(n):
    for i in range(n+1):
        if n%2==0:
            yield i
n=int(input())
print(",".join(str(x) for x in even(n)))