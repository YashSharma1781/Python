class Employee:
    company = "Google"

    def __init__(self, salary, name, bond, company):
        self.salary = salary
        self.name = name
        self.bond = bond
        self.company = company

e1 = Employee(200000, "lokesh", 3, "Tesla")
print(e1.company)

