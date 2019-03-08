import employee as emp 

e1_salary_json = {
    "entry1": {
        "company" : "Company 1", 
        "position" : "SDE Intern",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 10000,
        "employee_id" : 372545
    },
    "entry2": {
        "company" : "Student Agencies", 
        "position" : "Volunteer",
        "start" : "06/01/18",
        "end" : "08/27/18",
        "salary" : 0,
        "employee_id" : 372545
    }
}
e1_salary_history = (e1_salary_json)
e1 = emp.Employee(372545, emp.EmployeeTypes.EMPLOYEE, "employee1@gmail.com", "passwordhash", 
                 "Employee One", 10000.00, e1_salary_history, 40, 1000.00)

e2_salary_json = {
    "entry1": {
        "company" : "Company 2", 
        "position" : "Lead Engineer",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 40000,
        "employee_id" : 11234
    },
    "entry2": {
        "company" : "Company 3", 
        "position" : "Senior engineer",
        "start" : "06/01/18",
        "end" : "08/27/18",
        "salary" : 30000,
        "employee_id" : 11234
    }
}
e2_salary_history = (e2_salary_json)
e2 = emp.Employee(11234, emp.EmployeeTypes.EMPLOYEE, "employee2@gmail.com", "passwordhash", 
                 "Employee Two", 50000.00, e2_salary_history, 23, 2500.00)

e3_salary_json = {
    "entry1": {
        "company" : "Company 4", 
        "position" : "Product Manager",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 50000,
        "employee_id" : 55242
    },
}
e3_salary_history = (e3_salary_json)
e3 = emp.Employee(55242, emp.EmployeeTypes.EMPLOYEE, "employee3@gmail.com", "passwordhash", 
                 "Employee Three", 60000.00, e3_salary_history, 3, 4500.00)

m1_salary_json = {
    "entry1": {
        "company" : "Company 3", 
        "position" : "Product Manager",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 34252,
        "employee_id" : 77777
    },
}
m1_salary_history = (m1_salary_json)
m1 = emp.Employee(77777, emp.EmployeeTypes.MANAGER, "manager1@gmail.com", "passwordhash", 
                 "Manager One", 70000.00, m1_salary_history, 7, 7322.00, [e1, e2])

m2_salary_json = {
    "entry1": {
        "company" : "Company 7", 
        "position" : "Head of Engineering",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 100000,
        "employee_id" : 54321
    },
}
m2_salary_history = (m2_salary_json)
m2 = emp.Employee(54321, emp.EmployeeTypes.MANAGER, "manager2@gmail.com", "passwordhash", 
                 "Manager Two", 98435.00, m2_salary_history, 243, 10000.00, [e3])

hr1_salary_json = {
    "entry1": {
        "company" : "Company 3", 
        "position" : "Human Resources",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 34252,
        "employee_id" : 78787
    },
}
hr1_salary_history = (hr1_salary_json)
hr1 = emp.Employee(78787, emp.EmployeeTypes.HR, "hr1@gmail.com", "passwordhash", 
                 "HumanR One", 70000.00, hr1_salary_history, 7, 7322.00)

hr2_salary_json = {
    "entry1": {
        "company" : "Company 7", 
        "position" : "Head of Engineering",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 100000,
        "employee_id" : 65656
    },
}
hr2_salary_history = (hr2_salary_json)
hr2 = emp.Employee(65656, emp.EmployeeTypes.HR, "hr2@gmail.com", "passwordhash", 
                 "HumanR Two", 98435.00, hr2_salary_history, 243, 10000.00)


a1_salary_json = {
    "entry1": {
        "company" : "Company 23", 
        "position" : "Head of IT",
        "start" : "06/01/19",
        "end" : "08/27/19",
        "salary" : 1000000,
        "employee_id" : 99999
    },
}
a1_salary_history = (a1_salary_json)
a1 = emp.Employee(99999, emp.EmployeeTypes.ADMIN, "admin1@gmail.com", "passwordhash", 
                 "Admin One", 100000.00, a1_salary_history, 3, 100000.00)
