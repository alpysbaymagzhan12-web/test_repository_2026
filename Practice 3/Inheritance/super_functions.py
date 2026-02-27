class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        # Ата-ананың __init__ әдісін іске қосамыз
        super().__init__(name)
        self.grade = grade

    def info(self):
        print(f"Оқушы: {self.name}, Сыныбы: {self.grade}")

ali = Student("Әли", 10)
ali.info()