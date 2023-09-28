from building_scheduler.building import (
    CommercialBuilding,
    SingleStoreyHome,
    TwoStoreyHome,
)
from building_scheduler.building_scheduler import (
    BuildingScheduler,
)
from building_scheduler.roster import Employee, EmployeeRole, Roster


def test_simple_weekly_schedule():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
        }
    )
    buildings = {
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
    }
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    assert len(scheduler.daily_schedules["Monday"]) == 1
    assert len(scheduler.daily_schedules["Tuesday"]) == 1
    assert len(scheduler.daily_schedules["Wednesday"]) == 1
    assert len(scheduler.daily_schedules["Thursday"]) == 1
    assert len(scheduler.daily_schedules["Friday"]) == 1


def test_more_workers_complete_jobs_faster():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chelly"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charles"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chester"),
        }
    )
    buildings = {
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
        SingleStoreyHome(),
    }
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    assert len(scheduler.daily_schedules["Monday"]) == 4
    assert len(scheduler.daily_schedules["Tuesday"]) == 1
    assert len(scheduler.daily_schedules["Wednesday"]) == 0
    assert len(scheduler.daily_schedules["Thursday"]) == 0
    assert len(scheduler.daily_schedules["Friday"]) == 0


def test_absent_workers_move_work_to_next_day():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli", ["Monday"]),
        }
    )
    buildings = {
        SingleStoreyHome(),
    }
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    assert len(scheduler.daily_schedules["Monday"]) == 0
    assert len(scheduler.daily_schedules["Tuesday"]) == 1
    assert len(scheduler.daily_schedules["Wednesday"]) == 0
    assert len(scheduler.daily_schedules["Thursday"]) == 0
    assert len(scheduler.daily_schedules["Friday"]) == 0


def test_complex_requirements_can_be_satisfied():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chelly"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charles"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chester"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Agnes"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Arnold"),
            Employee(EmployeeRole.LABOURER, "Labourer Liam"),
            Employee(EmployeeRole.LABOURER, "Labourer Lindsay"),
        }
    )
    buildings = [
        SingleStoreyHome(),
        TwoStoreyHome(),
        CommercialBuilding(),
    ]
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    monday = scheduler.daily_schedules["Monday"]
    assert SingleStoreyHome in [type(s.building) for s in monday]
    assert TwoStoreyHome in [type(s.building) for s in monday]
    tuesday = scheduler.daily_schedules["Tuesday"]
    assert CommercialBuilding in [type(s.building) for s in tuesday]


def test_most_complex_building_pushes_work_later_in_week():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charli"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chelly"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Charles"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Certified Chester"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Agnes"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Arnold"),
            Employee(EmployeeRole.LABOURER, "Labourer Liam"),
            Employee(EmployeeRole.LABOURER, "Labourer Lindsay"),
        }
    )
    buildings = [
        CommercialBuilding(),
        SingleStoreyHome(),
        TwoStoreyHome(),
    ]
    scheduler = BuildingScheduler(buildings, roster)

    scheduler.generate_weekly_schedule()

    monday = scheduler.daily_schedules["Monday"]
    tuesday = scheduler.daily_schedules["Tuesday"]
    assert CommercialBuilding in [type(s.building) for s in monday]
    assert SingleStoreyHome in [type(s.building) for s in tuesday]
    assert TwoStoreyHome in [type(s.building) for s in tuesday]

