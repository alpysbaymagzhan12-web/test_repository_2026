class Camera:
    def take_photo(self):
        print("Суретке түсіру...")

class Player:
    def play_music(self):
        print("Музыка ойнату...")

# Екі кластан да мұра алады
class SmartDevice(Camera, Player):
    pass

phone = SmartDevice()
phone.take_photo()
phone.play_music()