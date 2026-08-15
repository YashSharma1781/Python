'''
number = int(input("enter the number="))

if number>0:
    print("positive")
    
elif number == 0:
    print("Zero")
    
else:
    print("negative")
    
# -------------------------------------------------------
    
# age = int(input("Enter your age="))

# if age>=18:
#     print("you can give vote")
    
# else:
#     print("you cannot give vote")
    
# ------------------------------------------------------

# num = int(input("enter a number="))

# if num % 2 == 0:
#     print("Number is even")
    
# else:
#     print("odd")
# -------------------------------------------------------
'''
# a = int(input("enter the number between 1 to 4="))
# match a:
    
#     case 1:
#         print("sunday")
        
#     case 2:
#         print("monday")

#     case 3:
#         print("tuesday")
        
#     case 4:
#         print("wednesday")
#---------------------------------------------------------
# num1 = int(input("Enter first number="))
# num2 = int(input("Enter second number="))
# calc = input("Enter your choice=")

# match calc:
#     case "+":
#         print("sum=",num1+num2)
            
#---------------------------------------------------------

# for i in range(1,11):
#     print(i)   
#---------------------------------------------------------

# num = int(input("enter the number of your choice="))
# for i in range(1,11):
#     print(num, "X", i, "=",num*i)
#---------------------------------------------------------
# num =0
# for i in range(1,101):
#     num+=i
    
# print(num)
#-------------------------------------------------------
# for i in range(1,5):
#     print("* "*i)
#-------------------------------------------------------

# i =1
# while i<=10:
#     print(i)
#     i+=1
#------------------------------------------------------
# password = 123456
# entered_pass = int(input("Enter pass: "))

# while entered_pass != password:
#     entered_pass = int(input("Wrong pass, try again: "))

# print("Logged in")
#------------------------------------------------------------
# num = 123456
# print(str(num)[::-1])
#-----------------------------------------------------------

# for i in range(1,11):
#     if i == 7:
#         break
#     print(i)
#----------------------------------------------------------
# for i in range(1,11):
#     if i == 5:
#         continue
#     print(i)
#--------------------------------------------------------
for i in range(1,6):
    match i:
        case 1:
            print(1)
        case 2:
            print(2)
        case 3:
            pass
        case 4:
            print(4)
            
        case 5:
            print(5)