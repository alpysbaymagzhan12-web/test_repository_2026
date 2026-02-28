from datetime import datetime

a1 = datetime(2026, 2, 28, 10, 55, 0)
a2 = datetime(2025, 5, 25, 5, 25, 0)

b = a1-a2
print("Айырма секундпен:", b.total_seconds())
