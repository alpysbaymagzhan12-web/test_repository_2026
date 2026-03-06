import re


with open('raw.txt', 'r', encoding='utf-8') as file:
    text = file.read()

def convert(match):
    
    return match.group(1).upper()


camel_case_text = re.sub(r"_([a-z])", convert, text)


print(camel_case_text)