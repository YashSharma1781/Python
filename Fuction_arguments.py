# positional arguments

def add(a,b):
    return a+b # a and b are parameters

c = add(10,20) # arguments
print(c)
    
    
# default arguments

def add(a1,b1,c1=9):
    return a1+b1+c1

sum = add(10,20,12)
print(sum)

# keyword arguments

def Student(name, age):
    print(f"name: {name} Age: {age}")
    
Student("yash", 20)


def Info(name, age, salary):
    print(f"name:{name},age:{age},salary:{salary}")
    
Info("laksh", 24, 95000)
Info("samay", 25, 150000)