import re


x = r'ab{2,3}'


y = ["abb", "abbb", "abbbb", "ab", "a", "b"]

for s in y:
    if re.fullmatch(x, s):
        print(f"'{s}' -> Match")
    else:
        print(f"'{s}' -> No match")
