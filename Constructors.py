class Employee:
    
    def __init__(self, salary,name,bond):
        self.salary=salary
        self.name=name
        self.bond=bond
        
    def get_salary(self):
        return self.salary
    
    def get_info(self):
        print(f"the name of employee is {self.name} and his salary is {self.salary} and his bond is for {self.bond} years")
    
e = Employee(250000,"rohan",3)
print(e.get_salary())
e.get_info()
e.get_salary()


class Student:
    
    def __init__(self, studentID, CGPA, Attendance):
        self.studentID=studentID
        self.CGPA=CGPA
        self.Attendance=Attendance
        
    def student_info(self):
            print(f"student name -{self.studentID}\nCGPA - {self.CGPA}\nAttendance - {self.Attendance}\n")
            
s = Student("laksh",8.6,99.6)
s1 = Student("rohan",9.12,99.8)
s.student_info()
s1.student_info()
