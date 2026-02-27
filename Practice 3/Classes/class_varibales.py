class Car:
    wheels = 4  # Класс айнымалысы (барлық көлікте 4 дөңгелек)

    def __init__(self, name):
        self.name = name  # Экземпляр айнымалысы (әр көліктің аты әртүрлі)

car1 = Car("Toyota")
car2 = Car("BMW")

print(car1.name, car1.wheels) # Toyota 4
print(car2.name, car2.wheels) # BMW 4