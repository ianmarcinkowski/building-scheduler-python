from enum import Enum


class NoEmployeeAvailable(Exception):
    pass


class EmployeeRole(Enum):
    CERTIFIED_INSTALLER = 1
    PENDING_INSTALLER = 2
    LABOURER = 3
    ANY = 4


ASSIGNABLE_EMPLOYEE_ROLES = [
    EmployeeRole.CERTIFIED_INSTALLER,
    EmployeeRole.PENDING_INSTALLER,
    EmployeeRole.LABOURER,
]


class Employee:
    def __init__(self, role: EmployeeRole, name: str, days_off: list[str] = []):
        self.role = role
        self.name = name
        self.days_off = days_off

    def __repr__(self):
        return f"{self.role}|{self.name}"

    def is_available(self, day, role_requirement):
        if self.fits_role(role_requirement) and day not in self.days_off:
            return True
        return False

    def fits_role(self, role_requirement):
        if role_requirement == EmployeeRole.ANY:
            return True
        elif self.role == role_requirement:
            return True
        elif type(role_requirement) == tuple and self.role in role_requirement:
            return True
        return False
