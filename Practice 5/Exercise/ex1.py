import re


x = r'ab*'


y = ["a", "ab", "abb", "abbb", "ac", "b", ""]

for s in y:
    if re.fullmatch(x, s):
        print(f"'{s}' -> Match")
    else:
        print(f"'{s}' -> No match")
