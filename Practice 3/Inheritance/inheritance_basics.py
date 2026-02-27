# Ата-ана класс
class Animal:
    def breathe(self):
        print("Тыныс алып жатыр...")

# Бала класс
class Bird(Animal):
    def fly(self):
        print("Ұшып барады...")

eagle = Bird()
eagle.breathe()  # Ата-анадан келген әдіс
eagle.fly()      # Өзінің әдісі