import datetime
import sys

try:
    str = 1
    raise Exception
    len(str)
    
except TypeError:
    print("You didn't give a str")
except Exception as e:  
    print('exception')

print(sys.executable)

class Student:
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.name = f'{firstname} {lastname}'

    


student1 = Student('Euan', 'Williams')
print(student1.name)