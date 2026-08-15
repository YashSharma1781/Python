a = int(input("Enter a lucky number="))

match a:
    case 10:
        print("Winner number is 10")
        
    case 16:
        print("runner up number is 16")
        
    case 9:
        print("Third winner number is 9")
        
    case 13:
        print("bonus winner number is 13")
    
        
    case _:
        print("number not found!!!..Better luck next time")
        
    