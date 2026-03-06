import re
with open('raw.txt', 'r', encoding='utf-8') as f:
    a = f.read()
print(re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", a).lower())