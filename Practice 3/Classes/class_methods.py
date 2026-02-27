class Dog:
    def __init__(self, name):
        self.name = name

    # Бұл — әдіс (method)
    def bark(self):
        return f"{self.name}: Гав-гав!"

    def eat(self, food):
        return f"{self.name} {food} жеп жатыр."

my_dog = Dog("Ақтөс")
print(my_dog.bark())
print(my_dog.eat("сүйек"))