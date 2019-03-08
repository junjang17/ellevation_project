import sqlite3
from employee import EmployeeTypes, Employee

# Dictionary to emulate session tokens
APP_CONFIG = {"curr_user_id":None, "curr_user_privilege":None}

class Error(Exception):
   """Base class for other exceptions"""
   pass

class InvalidPrivilege(Error):
   """Raised when the user performs actions that they don't have permission for"""
   pass

class InsertError(Error):
    """Raised when a table insert fails"""
    pass

def login_required(f):
    """
    Decorate routes to require login.
    """
    def decorated_function(*args, **kwargs):
        if APP_CONFIG["curr_user_id"] is None:
            raise InvalidPrivilege ("Not logged in")
        return f(*args, **kwargs)
    return decorated_function

def login(email, password):
    """
    Simulates Logging in to webapp. 
    
    Validate email from database, and validate hash of password.
    Store user's id and privilege level in session (APP_CONFIG)

    Parameters: 
        email (string): User's log in credentials
        password (string): Hash of password to authenticate

    Return: None
    """
    if APP_CONFIG["curr_user_id"] != None:
        return
    conn = sqlite3.connect(r"app_database")
    sql = "SELECT * FROM user WHERE email=?"
    rows = conn.cursor().execute(sql, (email,)).fetchall()

    if not rows:
        return False
    else:
        row = rows[0]
        if password != row[-1]:
            return InvalidPrivilege ("Login Failed")
        APP_CONFIG["curr_user_id"] = row[0]
        APP_CONFIG["curr_user_privilege"] = row[1]
    
    return

def logout():
    """
    Simulates Logging out of webapp.
    
    Clear the session (APP_CONFIG) since log in checks whether 
    curr_user_id is set to a value other than None.

    Parameters: None

    Return: None
    """
    for key in APP_CONFIG:
        APP_CONFIG[key] = None

    return

@login_required
def register(employee):
    """
    Registers an employee into the database.
    
    Only Admins can register other users into the system.
    The values from the requested employee object are extracted, 
    and relevant data are stored to the corresponding db tables.

    Parameters: 
        employee (Employee): Employee object to register into db

    Return: None
    """
    if APP_CONFIG["curr_user_privilege"] != EmployeeTypes.ADMIN:
        raise InvalidPrivilege ("Only admins can perform this action")
    conn = sqlite3.connect(r"app_database")
    c = conn.cursor().execute("SELECT EXISTS(SELECT 1 FROM user WHERE employee_id=?)", 
                                                        (employee.employee_id,))
    if c.fetchone()[0]:
        raise InsertError ("Employee already registered")
    if employee.employee_list: 
        if employee.employee_privilege != EmployeeTypes.MANAGER:
            raise InvalidPrivilege ("Only Managers have employees")
        else:
            for e in employee.employee_list:
                row_vals = {
                    "employee_id" : e.employee_id,
                    "manager_id" : employee.employee_id
                }
                conn = sqlite3.connect(r"app_database")
                sqlite_insert(conn, "employee_manager", row_vals)
    
    user_vals = {
        "employee_id" : employee.employee_id,
        "employee_privilege" : employee.employee_privilege, 
        "email" : employee.email,
        "password" : employee.password
    }
    employee_info_vals = {
        "employee_id" : employee.employee_id,
        "name" : employee.name,
        "salary" : employee.salary,
        "vacation_balance" : employee.vacation_balance,
        "annual_bonus" : employee.annual_bonus
    }
    conn = sqlite3.connect(r"app_database")
    sqlite_insert(conn, "user", user_vals)
    sqlite_insert(conn, "employee_info", employee_info_vals)

    return 

@login_required
def get_employee_information(employee, fields):
    """
    Retrieve an employee's information, and returns JSON object.
    
    All employees can view their own info.
    Managers can view info of employees they manage.
    HR can view all other employees' data except other HR employees.
    Admins can view all info.

    Parameters: 
        employee (Employee): Object to retrieve data about
        fields (string list): list of database columns to query
    
    Return: Nested JSON object of index and information
        ex. {0: {salary : 400}}
    """
    privilege = APP_CONFIG["curr_user_privilege"]
    if privilege == EmployeeTypes.EMPLOYEE:
        if APP_CONFIG["curr_user_id"] != employee.employee_id:
            raise InvalidPrivilege ("No privilege to access information")
    elif privilege == EmployeeTypes.HR:
        if employee.employee_privilege == EmployeeTypes.HR:
            raise InvalidPrivilege ("Cannot Access HR information")
    elif privilege == EmployeeTypes.MANAGER:
        if not is_under_manager(APP_CONFIG["curr_user_id"], employee):
            raise InvalidPrivilege ("Employee not under manager")

    conn = sqlite3.connect(r"app_database")
    rows = sqlite_select(conn, "employee_info", fields, "employee_id", employee.employee_id)
    
    return jsonify(fields, rows)

@login_required
def set_employee_information(employee, key, value):
    """ 
    Helper function to enter salary history into salary_history table. 
  
    Parameters: 
        employee (Employee object): Employee to change information for
        key (string): column of employee_info to change 
        value (?): value of column to enter (type is polymorphic)
    Returns: None
    """
    privilege = APP_CONFIG["curr_user_privilege"]
    if privilege == EmployeeTypes.EMPLOYEE or privilege == EmployeeTypes.HR:
        raise InvalidPrivilege ("No privilege to set information")
    if privilege == EmployeeTypes.MANAGER:
        if not is_under_manager(APP_CONFIG["curr_user_id"], employee):
            raise InvalidPrivilege ("Employee not under manager")
        allowed_keys = ["name", "salary", "vacation_balance", "annual_bonus"]
        if key not in allowed_keys:
            raise InvalidPrivilege ("No privilege to set information")
    
    conn = sqlite3.connect(r"app_database")
    sql = "UPDATE employee_info SET {}=? WHERE employee_id=?".format(key)
    conn.cursor().execute(sql, (value,employee.employee_id))
    conn.commit()

    return

@login_required
def enter_salary_history(entry):
    """ 
    Helper function to enter salary history into salary_history table. 
  
    Parameters: 
        entry (string dict): key, value pairs of database columns and 
                             corresponding values 
    Returns: None
    """
    conn = sqlite3.connect(r"app_database")
    sqlite_insert(conn, "salary_history", entry)

    return

@login_required
def get_salary_history(employee):
    """ 
    Retrieves salary history about an employee. 
  
    Parameters: 
        employee (Employee object): Employee to get salary_history about
    Returns: Nested JSON object of each salary history entry for the employee
    """
    privilege = APP_CONFIG["curr_user_privilege"]
    if privilege == EmployeeTypes.EMPLOYEE:
        if APP_CONFIG["curr_user_id"] != employee.employee_id:
            raise InvalidPrivilege ("No privilege to access information")
    elif privilege == EmployeeTypes.HR:
        if employee.employee_id == EmployeeTypes.HR:
            raise InvalidPrivilege ("Cannot Access HR information")
    elif privilege == EmployeeTypes.MANAGER:
        if not is_under_manager(APP_CONFIG["curr_user_id"], employee):
            raise InvalidPrivilege ("Employee not under manager")
    conn = sqlite3.connect(r"app_database")
    sql = "SELECT company, position, start, end, salary \
           FROM salary_history WHERE employee_id=?"
    c = conn.cursor().execute(sql, (employee.employee_id,))
    rows = c.fetchall()

    return jsonify(["company", "position", "start", "end", "salary"], list(rows))

@login_required
def set_manager_employees(manager, employee):
    """ 
    Helper function to set a manager's employees. 
  
    Parameters: 
        manager (Employee object): Manager to add employees to 
        employee (Employee object): Employee to be added
    Returns: None
    """
    if APP_CONFIG["curr_user_privilege"] != EmployeeTypes.ADMIN:
        raise InvalidPrivilege ("No privilege for action")
    conn = sqlite3.connect(r"app_database")
    sql = "INSERT INTO employee_manager (employee_id, manager_id) \
           VALUES (?, ?)"
    conn.cursor().execute(sql, (employee.employee_id, manager.employee_id))
    conn.commit()
    conn.close()
    
    return

@login_required
def set_privilege(employee, privilege):
    """ 
    Changes another user's permission. Only Admins can perform this action.
  
    Parameters: 
        employee (Employee object): Employee to change privilege
        privilege (int): New Enum EmployeeType to change privilege to
    Returns: None
    """
    if APP_CONFIG["curr_user_privilege"] != EmployeeTypes.ADMIN:
        raise InvalidPrivilege
    employee.employee_privilege = privilege

def sqlite_insert(conn, table, row):
    """ 
    Helper function to insert into sqlite3 table.
    *    Title: <sqlite_insert>
    *    Author: <stil>
    *    Date Accessed: <03/05/2019>
    *    URL: <https://stackoverflow.com/questions/2092757/python-and-sqlite-insert-into-table>
    
    Parameters: 
        conn (Connection object): Object representing connection to db
        table (string): Table to insert into
        row (string dict): Column, row pairings to enter into
    Returns: None
    """
    # validate table, row before
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()
    conn.cursor().close()

    return

def sqlite_select(conn, table, fields, col, identifier):
    """ 
    Helper function to select information from sqlite database.

    Parameters: 
        conn (Connection object): Object representing connection to db
        fields (string list): Columns to select
        table (string): Table to select from
        col (string dict): Column to select by
        identifier (string): Column value to select by
    Returns: None
    """
    fields = ', '.join(fields)
    sql = "SELECT {0} FROM {1} WHERE {2}=?".format(fields, table, col)
    c = conn.cursor().execute(sql, (identifier,))
    rows = c.fetchall()
    conn.cursor().close()
    
    return rows

def clean_name(some_var):
    """
    Helper function to sanitize SQL inputs
    
    Parameters:
        some_var (string): String to sanitize
    Return: sanitized string
    """
    
    return ''.join(char for char in some_var if char.isalnum())

def sql_to_list(sql_out):
    """
    Helper function to change sql output (tuple list) into list of lists

    Parameters:
        sql_out (tuple list): List of tuples containing various types
    Return: List of lists containing original tuple elements
    """
    ret = []
    for tup in sql_out:
        ret.append(list(tup))
    
    return ret

# Given a list of keys and sql select output, return json
def jsonify(keys, vals):
    """
    Helper function to create JSON style string output (for webapp purposes)

    Parameters:
        keys (string list): List of strings containing key names
        vals (string list): List of values
    Return: Nested JSON style dictionary
    """
    vals = sql_to_list(vals)
    json = {}
    for i in range(len(vals)):
        inner_json = {}
        assert(len(keys) == len(vals[i]))
        k = 0
        while k < len(keys):
            inner_json[keys[k]] = str(vals[i][k])
            k += 1
        json[i] = inner_json
    
    return json

def is_under_manager(manager_id, employee):
    """
    Helper function to determine if employee belongs to manager

    Parameters:
        manager_id (int): ID of Manager to check
        employee (Employee object): Employee to verify
    Return: Boolean
    """
    conn = sqlite3.connect(r"app_database")
    sql = "SELECT EXISTS(SELECT 1 FROM employee_manager WHERE \
                              employee_id=? AND manager_id=?)"
    c = conn.cursor().execute(sql, (employee.employee_id, manager_id))
    if c.fetchone()[0] == 0:
        return False
    
    return True

def create_employee_obj(employee_id):
    """
    Helper function to create Employee Object using information in database

    Parameters:
        employee_id (int): ID of employee to be made into object
    Return: Employee object
    """
    conn = sqlite3.connect(r"app_database")
    sql = "SELECT user.employee_id, employee_privilege, email, password, name, salary, \
                vacation_balance, annual_bonus FROM user INNER JOIN employee_info \
           ON user.employee_id=? AND user.employee_id=employee_info.employee_id"
    c = conn.cursor().execute(sql, (employee_id,))
    rows = c.fetchall()[0]
    json = {
        "employee_id":employee_id,
        "employee_privilege":None,
        "email":None,
        "password":None,
        "name":None,
        "salary":None,
        "vacation_balance":None,
        "annual_bonus":None
    }
    keys = list(json.keys())
    i = 0
    while i < len(keys):
        key = keys[i]
        json[key] = rows[i]
        i += 1
    employee = Employee(*rows, None)

    return employee
