class Employee:
    company = "HP"
    
    def get_salary(self):
        return 34000
    
e= Employee()
e2 = Employee()
print(e.get_salary())
print(e2.get_salary())