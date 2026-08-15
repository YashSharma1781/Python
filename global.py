def sum(a, b):
    print("adding two numbers")
    c =a+b
    global z
    z =0
    return c

z=3
print(sum(10,20))
print(z)