from datetime import datetime

n= datetime.now()
y = n.replace(microsecond=0)

print("Қазір:", n)
print("Микросекундсыз:", y)
