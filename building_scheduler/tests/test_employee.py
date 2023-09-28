from building_scheduler.employee import Employee, EmployeeRole


def test_is_available():
    employee = Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Flavian")

    assert employee.is_available("Monday", EmployeeRole.CERTIFIED_INSTALLER)

def test_has_day_off():
    employee = Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Flavian", ["Tuesday"])

    assert not employee.is_available("Tuesday", EmployeeRole.CERTIFIED_INSTALLER)

def test_is_wrong_role():
    employee = Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Flavian")

    assert not employee.is_available("Wednesday", EmployeeRole.LABOURER)

def test_any_role():
    employee = Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Flavian")

    assert employee.is_available("Thursday", EmployeeRole.ANY)
