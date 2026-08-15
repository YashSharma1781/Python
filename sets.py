s = {3,2,22,34}
print(s,type(s))


# set methods

a = {12,32,43,54}
a.add(11)
a.remove(12)
a.discard(1234)
a.pop()
print(a)

# set oprations

x = {3,23,1}
y = {23, 4 , 2, 55, 1}
print(x.union(y))
print(x.intersection(y))