class Phone:
    def ring(self):
        print("Стандартты қоңырау дыбысы")

class iPhone(Phone):
    def ring(self):
        # Ата-ананың әдісін өзгерту
        print("Marimba рингтоны ойнап тұр")

my_phone = iPhone()
my_phone.ring() # Нәтиже: Marimba рингтоны ойнап тұр