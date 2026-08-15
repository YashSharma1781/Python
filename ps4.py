class car:
    def drive(self):
        print("car is moving")
        
c = car()
c.drive()

class person:
    def __init__(self,name,age):
        self.name =name
        self.age = age
        
p1 = person("yash",19)
print(p1.name, p1.age)


class Animal:
    def sound(self):
        print("some sound")
        
class dog:
    def sound(self):
        print("bark")
        
a = Animal()
a.sound()

b = dog()
b.sound()
