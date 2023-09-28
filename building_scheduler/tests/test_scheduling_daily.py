from building_scheduler.building import CommercialBuilding, SingleStoreyHome, TwoStoreyHome
from building_scheduler.building_scheduler import (
    BuildingScheduler,
)
from building_scheduler.employee import Employee, EmployeeRole
from building_scheduler.roster import Roster



def test_commercial_building():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Alex"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Arthur"),
            Employee(EmployeeRole.LABOURER, "Labourer Lily"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ianuchi"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Alpaca"),
            Employee(EmployeeRole.LABOURER, "Labourer Louis"),
        }
    )
    building = CommercialBuilding()
    scheduler = BuildingScheduler({building}, roster)

    schedule = scheduler.generate_daily_schedule("Thursday")

    assert len(schedule) == 1
    assert len(schedule[0].employees) == len(building.worker_requirements)


def test_two_storey_home():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
            Employee(EmployeeRole.LABOURER, "Labourer Lily"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Alex"),
        }
    )
    building = TwoStoreyHome()
    scheduler = BuildingScheduler({building}, roster)

    schedule = scheduler.generate_daily_schedule("Monday")

    assert len(schedule) == 1
    assert len(schedule[0].employees) == len(building.worker_requirements)


def test_single_storey_home():
    roster = Roster({Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian")})
    building = SingleStoreyHome()
    scheduler = BuildingScheduler({building}, roster)

    schedule = scheduler.generate_daily_schedule("Monday")

    assert len(schedule) == 1
    assert schedule[0].employees[0].name == "Installer Ian"
    assert len(schedule[0].employees) == len(building.worker_requirements)


def test_not_enough_workers_leaves_remaining_building():
    roster = Roster({Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian")})
    building_a = SingleStoreyHome()
    building_b = SingleStoreyHome()
    scheduler = BuildingScheduler({building_a, building_b}, roster)

    building_schedules = scheduler.generate_daily_schedule("Tuesday")

    assert len(building_schedules) == 1
    assert len(building_schedules[0].employees) == 1
    assert len(scheduler.remaining_buildings) == 1


def test_schedule_one_worker_can_work_different_days():
    roster = Roster({Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian")})
    building_a = SingleStoreyHome()
    building_b = SingleStoreyHome()
    scheduler = BuildingScheduler({building_a, building_b}, roster)

    wed_schedule = scheduler.generate_daily_schedule("Wednesday")
    thurs_schedule = scheduler.generate_daily_schedule("Thursday")

    assert len(wed_schedule) == 1
    assert len(thurs_schedule) == 1
    assert len(wed_schedule[0].employees) == 1
    assert len(thurs_schedule[0].employees) == 1


def test_schedule_multiple_buildings_sufficient_workers():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Abi"),
        }
    )
    building_a = SingleStoreyHome()
    building_b = SingleStoreyHome()
    scheduler = BuildingScheduler({building_a, building_b}, roster)

    schedule = scheduler.generate_daily_schedule("Thursday")

    assert len(schedule) == 2


def test_tracking_scheduled_buildings():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Abi"),
        }
    )
    building_a = SingleStoreyHome()
    building_b = SingleStoreyHome()
    scheduler = BuildingScheduler({building_a, building_b}, roster)

    scheduler.generate_daily_schedule("Monday")

    assert len(scheduler.scheduled_buildings) == 2


def test_tracking_scheduled_buildings_across_days():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
        }
    )
    building_a = SingleStoreyHome()
    building_b = SingleStoreyHome()
    scheduler = BuildingScheduler({building_a, building_b}, roster)

    scheduler.generate_daily_schedule("Monday")
    scheduler.generate_daily_schedule("Friday")

    assert len(scheduler.scheduled_buildings) == 2


def test_schedule_by_building_without_met_requirements():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.LABOURER, "Labourer Lily"),
        }
    )
    building = CommercialBuilding()
    scheduler = BuildingScheduler({building}, roster)

    schedule = scheduler.generate_daily_schedule("Thursday")

    assert len(schedule) == 0

