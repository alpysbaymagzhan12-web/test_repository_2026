import re
with open('raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()
print(re.findall(r"ab{2,3}", text))
