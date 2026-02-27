numbers = [1, 5, 8, 12, 15, 20]

# Тек 10-нан үлкен сандарды сүзгіден өткізу
greater_than_ten = list(filter(lambda x: x > 10, numbers))

print(greater_than_ten)  # Нәтиже: [12, 15, 20]