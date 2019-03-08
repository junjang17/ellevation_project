# Ellevation Technical Exercise

## Overview
The technical exercise was completed using python and SQLite3. I created a webapp simulation -- although an actual web server or framework was not set up, I wrote my code with principles of web backend programming in mind (session storage, login/logout authentication, .  

app.py - The main file with the fundamental logic of the webapp (functions to set/retrieve data, authenticating, permissions)
tests.py - Bare bones unit testing to ensure that basic functionality is met (as outlined in the prompt)
employee.py - Class definition of Employee Object
employee_defs.py - instantiation of numerous employee objects for testing purposes

## Design
My approach to the webapp was to create one employee class since the 4 types of employees (admin, manager, HR, regular employee) all had similar attributes to be tracked (salary, salary_history, vacation_balance, annual_bonus). The employee information was stored in a database table (employee_table) while authentication information (username, password, etc) was stored in a separate user table. The table salary_history stores all records of employees' previous history entries (per company) that is linked by employee ID such that a salary history can be generated. The employee_manager table stores managers' ids to employees' ids in a one-to-many relationship so that managers' employee lists can be generated as well.

### General Flow
Upon login, the employee's username and password allows for retrieval of the employee's unique id and privilege (aka employee type). The unique id and privilege are stored in the session (to save from constant database lookups). With the user's permission stored in the session, each time the user tries to call a function (viewing info, updating info, etc), the permission is checked in the function to prevent misuse of the system.

### Assumptions
	-Each employee has a unique ID in the company to identify the employee by

## Things to Improve
	- More rigorous testing: Although basic functionality has been tested for, not all aspects of the webapp have unit tests.
	- Sanitizing SQL inputs
	




