class Animal:
    breed = "german"
    def __init__(self,name):
        self.name = name
    def speak(self):
        print("Speaking now...")
        
class Dog(Animal):
    def speak(self):
        super().speak()
        print("WOOF!")
        
d = Dog("bruno")
d.speak()
print(d.breed)