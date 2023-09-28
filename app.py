import pprint
from building_scheduler.employee import Employee, EmployeeRole
from building_scheduler.roster import Roster
from building_scheduler.building_scheduler import BuildingScheduler
from building_scheduler.building import (
    CommercialBuilding,
    SingleStoreyHome,
    TwoStoreyHome,
)

def schedule(buildings: list, employees: set):
    roster = Roster(employees)
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    print("******** Weekly Schedule ********")
    print(scheduler.daily_schedules)
    print("Remaining Buildings")
    print(scheduler.remaining_buildings)

    print("******** Prettier, slightly out of order output ********")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(scheduler.daily_schedules)
    print("Remaining Buildings")
    pp.pprint(scheduler.remaining_buildings)

if __name__ == "__main__":
    buildings = [
        CommercialBuilding(),
        CommercialBuilding(),
        CommercialBuilding(),
        CommercialBuilding(),
        TwoStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        TwoStoreyHome(),
    ]

    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chelly"),
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charles"),
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chester"),
        Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Agnes"),
        Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Arnold"),
        Employee(EmployeeRole.LABOURER, "Labourer Liam", ["Monday"]),
        Employee(EmployeeRole.LABOURER, "Labourer Lindsay"),
    }

    schedule(buildings, employees)