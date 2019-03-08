# Enumeration for employee types
def enum(**enums):
    return type('Enum', (), enums)
EmployeeTypes = enum(ADMIN=0, MANAGER=1, HR=2, EMPLOYEE = 3) 

# Employee class representing the employee object holding pertinent data
class Employee:
    def __init__(self, employee_id, employee_privilege, email, password, name, 
                 salary, salary_history, vacation_balance, annual_bonus, employee_list=None):
        self.email = email
        self.password = password
        self.employee_id = employee_id
        self.employee_privilege = employee_privilege
        self.name = name
        self.salary = salary
        self.salary_history = salary_history
        self.vacation_balance = vacation_balance
        self.annual_bonus = annual_bonus
        self.employee_list = employee_list
