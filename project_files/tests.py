import app
import employee as emp 
from employee_defs import e1, e2, e3, m1, m2, hr1, hr2, a1
import unittest

#The unit tests below work with the employees registered in the database:
# employee 1, 2, 3; manager 1, 2; hr 1, 2; admin 1;

class Registration(unittest.TestCase):
    """ 
    Tests that registration permission is only given to admin. 
    """
    def test_no_login(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.register(e1)
    def test_employee_registration(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(e1.email, e1.password)
            app.register(e1)
    def test_hr_registration(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(hr1.email, hr1.password)
            app.register(e1)
    def test_manager_registration(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(m1.email, m1.password)
            app.register(e1)
    def test_admin_registration(self):
        with self.assertRaises(app.InsertError):
            # Expected to fail since e1 is already registered
            app.logout()
            app.login(a1.email, a1.password)
            app.register(e1)

class EmployeeInfoManipulation(unittest.TestCase):
    """ 
    Admins can see and edit any employee's data. Managers can only view and
    edit employees they are in charge of. HR and regular Employees cannot edit.

    Note: manager1(m1) is in charge of employee1(e1) and employee2(e2) but not
    employee3(m3)
    """
    def test_admin_changing_info(self):
        app.logout()
        app.login(a1.email, a1.password)
        app.set_employee_information(e1, "salary", 23333.3)
        row = app.get_employee_information(e1, ["salary"])[0] 
        assert(float(row["salary"]) == 23333.3)
        app.set_employee_information(e1, "salary", 12312.33)
        row = app.get_employee_information(e1, ["salary"])[0] 
        assert(float(row["salary"]) == 12312.33)
    def test_manager_changing_info_correct_employee(self):
        app.logout()
        app.login(m1.email, m1.password)
        app.set_employee_information(e1, "salary", 23333.3)
        row = app.get_employee_information(e1, ["salary"])[0] 
        assert(float(row["salary"]) == 23333.3)
        app.set_employee_information(e1, "salary", 12312.33)
        row = app.get_employee_information(e1, ["salary"])[0] 
        assert(float(row["salary"]) == 12312.33)
    def test_manager_changing_info_wrong_employee(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(m2.email, m2.password)
            app.set_employee_information(e1, "salary", 23333.3)
            row = app.get_employee_information(e1, ["salary"])[0] 
            assert(float(row["salary"]) == 23333.3)
            app.set_employee_information(e1, "salary", 12312.33)
            row = app.get_employee_information(e1, ["salary"])[0] 
            assert(float(row["salary"]) == 12312.33)
    def test_manager_changing_info_wrong_employee_2(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(m2.email, m2.password)
            app.set_employee_information(hr1, "salary", 23333.3)
            row = app.get_employee_information(hr1, ["salary"])[0] 
            assert(float(row["salary"]) == 23333.3)
            app.set_employee_information(hr1, "salary", 12312.33)
            row = app.get_employee_information(hr1, ["salary"])[0] 
            assert(float(row["salary"]) == 12312.33)
    def test_hr_changing_info(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(hr1.email, hr1.password)
            app.set_employee_information(e1, "salary", 23333.3)
    def test_employee_changing_info(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(e1.email, e1.password)
            app.set_employee_information(e1, "salary", 23333.3)
class EmployeeInfoView(unittest.TestCase):
    """ 
    Admins can see any employee's data. Managers can only view own data and data
    of employees they are in charge of. Regular employees can only see their data.
    HR workers can see everyone's data except other HR employees' data.

    Note: manager1(m1) is in charge of employee1(e1) and employee2(e2) but not
    employee3(m3)
    """
    def test_admin_viewing_info(self):
        app.logout()
        app.login(a1.email, a1.password)
        row = app.get_employee_information(e1, ["vacation_balance"])[0] 
        assert(int(row["vacation_balance"]) == 40)
    def test_manager_viewing_info_correct_employee(self):
        app.logout()
        app.login(m1.email, m1.password)
        row = app.get_employee_information(e2, ["salary"])[0] 
        assert(float(row["salary"]) == 50000.0)
    def test_manager_changing_info_wrong_employee(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(m2.email, m2.password)
            row = app.get_employee_information(e1, ["salary"])[0] 
            assert(float(row["salary"]) == 23333.3)
    def test_hr_viewing_info_admin(self):
        app.logout()
        app.login(hr1.email, hr1.password)
        app.get_employee_information(a1, ["salary"])
    def test_hr_viewing_info_hr(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(hr1.email, hr1.password)
            app.get_employee_information(hr2, ["salary"])
    def test_employee_viewing_info_self(self):
        app.logout()
        app.login(e1.email, e1.password)
        app.get_employee_information(e1, ["annual_bonus"])
        row = app.get_employee_information(e1, ["annual_bonus"])[0] 
        assert(float(row["annual_bonus"]) == 1000.0)
    def test_employee_viewing_info_employee(self):
        with self.assertRaises(app.InvalidPrivilege):
            app.logout()
            app.login(e1.email, e1.password)
            app.get_employee_information(e3, ["annual_bonus"])
            row = app.get_employee_information(e1, ["annual_bonus"])[0] 
            assert(float(row["annual_bonus"]) == 1000.0)

unittest.main(exit=False)
