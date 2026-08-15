def add(a,b):
    # a and b are local variables
    c=a+b
    z=1 # it destroyes itself

    return a
# z is a global variable
z = 100
print(add(10,20))
print(z)