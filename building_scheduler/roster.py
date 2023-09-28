from typing import Set
from building_scheduler.employee import (
    Employee,
    EmployeeRole,
    ASSIGNABLE_EMPLOYEE_ROLES,
)


class NoEmployeeAvailable(Exception):
    pass


class Roster:
    def __init__(self, employees: Set[Employee]):
        self.employees = employees
        self.scheduled = {
            "Monday": set(),
            "Tuesday": set(),
            "Wednesday": set(),
            "Thursday": set(),
            "Friday": set(),
        }

    def schedule_employee(self, day: str, role=EmployeeRole.ANY) -> Employee:
        available = self.get_available_employees(day, role)
        if len(available) == 0:
            raise NoEmployeeAvailable

        first_available = next(iter(available))
        self.scheduled[day].add(first_available)
        return first_available

    def get_available_employees(self, day, role) -> Set:
        available_employees = {
            emp for emp in self.employees if emp.is_available(day, role)
        }
        if role in ASSIGNABLE_EMPLOYEE_ROLES:
            return available_employees - {
                emp for emp in self.scheduled[day] if emp.role == role
            }
        return available_employees - {emp for emp in self.scheduled[day]}

    def meets_worker_requirements(self, day: str, required_workers: list) -> bool:
        requirements_met = True
        available = {}
        available[EmployeeRole.CERTIFIED_INSTALLER] = self.get_available_employees(
            day, EmployeeRole.CERTIFIED_INSTALLER
        )
        available[EmployeeRole.PENDING_INSTALLER] = self.get_available_employees(
            day, EmployeeRole.PENDING_INSTALLER
        )
        available[EmployeeRole.LABOURER] = self.get_available_employees(
            day, EmployeeRole.LABOURER
        )

        for requirement in required_workers:
            # TODO typechecking here indicates that I need a new abstraction
            # to handle a "worker requirement slot" but that can be post-MVP
            if requirement is EmployeeRole.ANY:
                any_requirement_met = False
                for role in ASSIGNABLE_EMPLOYEE_ROLES:
                    if len(available[role]) > 0:
                        available[role].pop()
                        any_requirement_met = True
                        break
                requirements_met = requirements_met and any_requirement_met
            elif type(requirement) is EmployeeRole:
                if len(available[requirement]) > 0:
                    available[requirement].pop()
                else:
                    requirements_met = False
            elif type(requirement) is tuple:
                or_requirement_met = False
                for or_requirement in requirement:
                    if len(available[or_requirement]) > 0:
                        available[or_requirement].pop()
                        or_requirement_met = True
                        break
                requirements_met = requirements_met and or_requirement_met

        return requirements_met
