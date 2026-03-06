import re
with open('raw.txt', 'r', encoding='utf-8') as f:
    a = f.read()
print(re.findall(r"a.*b", a))