class Student:
    clg="MES"
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def display(self):
        place="calicut"
        return f"Age of {self.name} is {self.age} ,from {place}"
        # print("name:",self.name)
        # print("age:",self.age)
        # print("place:",place)

    def marks(self,mark):
        return f"{mark} marks in subjects"
        # print(mark)
    
obj=student("anu",22)
# obj.display()
print(obj.display())
print(obj.marks(50))
# print(student.clg)

