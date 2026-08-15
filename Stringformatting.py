tempplate = "Dear {}, you are great. take this  {}$ bag"

a = "john"
a1 = 10000
b = "jack"
b1 = 1000
c = "marrie"                               #------------> formatting
c1 = 300

s1 = tempplate.format(a,a1)
print(s1)

print(f"{b} you are great, this is your {b1}$ reward") #----------f-string