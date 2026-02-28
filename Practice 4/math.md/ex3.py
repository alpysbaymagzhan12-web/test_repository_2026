import math

n = int(input("input number of sidez="))
s = int(input("Input the length a side="))

a = (n * s**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", a)
