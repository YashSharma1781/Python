marks = [100, 89,97,78,88]
mixed = [45, "hello",False,4.2]

print(marks[0])
print(mixed[2])
print(marks[2:4])

# list methods

mark = [10,22,33,5,17]
# mark.append(15)
# mark.pop()
print(mark)

my_list = [1, 2, 3]

my_list.append(4)   # [1, 2, 3, 4]
my_list.insert(1, 99)  # [1, 99, 2, 3, 4]
my_list.remove(2)   # [1, 99, 3, 4]
my_list.pop()       # Removes last element -> [1, 99, 3]
my_list.reverse()   # [3, 99, 1]
my_list.sort()      # [1, 3, 99]
print(my_list)

# list comprehension
# a = 5
# table = []

# for i in range(1,11):
#     table.append(5*i)
    
# print(table)

table = [5*i for i in range(1,11)]
print(table)