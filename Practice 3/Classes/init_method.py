class SmartPhone:
    def __init__(self, brand, model):
        self.brand = brand  # Экземпляр айнымалысы
        self.model = model
        print(f"{self.brand} {self.model} жасалды!")

phone1 = SmartPhone("Apple", "iPhone 15")
phone2 = SmartPhone("Samsung", "S24")