import re
with open('raw.txt', 'r', encoding='utf-8') as f:
    a = f.read()
b=(re.findall(r"ab*", a,re.I))
print(b)

