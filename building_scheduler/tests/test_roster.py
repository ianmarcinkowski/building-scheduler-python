import pytest
from building_scheduler.roster import (
    Employee,
    EmployeeRole,
    Roster,
    NoEmployeeAvailable,
)


def test_schedules_employee():
    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Abi"),
    }
    roster = Roster(employees)

    got = roster.schedule_employee("Monday")

    assert got.name == "Installer Abi"


def test_employee_on_leave():
    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Bill", ["Monday"]),
    }
    roster = Roster(employees)

    with pytest.raises(NoEmployeeAvailable):
        roster.schedule_employee("Monday", EmployeeRole.ANY)


def test_schedule_by_role():
    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Bill"),
        Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Ella"),
        Employee(EmployeeRole.LABOURER, "Labourer Kotol"),
    }
    roster = Roster(employees)

    got = roster.schedule_employee("Tuesday", EmployeeRole.PENDING_INSTALLER)

    assert got.name == "Apprentice Ella"


def test_schedule_first_available_any_role():
    employees = {
        Employee(EmployeeRole.LABOURER, "Labourer Kotol"),
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Bill"),
        Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Ella"),
    }
    roster = Roster(employees)

    roster.schedule_employee("Tuesday", EmployeeRole.ANY)
    roster.schedule_employee("Tuesday", EmployeeRole.ANY)

    tuesday = roster.scheduled["Tuesday"]
    assert len(tuesday) == 2


def test_no_employee_available():
    employees = set()
    roster = Roster(employees)

    with pytest.raises(NoEmployeeAvailable):
        roster.schedule_employee("Wednesday")


def test_no_employee_available_of_role():
    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Champ"),
        Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Efram"),
    }
    roster = Roster(employees)

    with pytest.raises(NoEmployeeAvailable):
        roster.schedule_employee("Thursday", EmployeeRole.LABOURER)


def test_schedule_employee_is_not_available():
    employee = Employee(EmployeeRole.CERTIFIED_INSTALLER, "Solo Installer")
    roster = Roster({employee})
    roster.scheduled["Monday"] = {employee}

    available = roster.get_available_employees("Monday", EmployeeRole.ANY)
    assert len(available) == 0


def test_get_available_employees_by_role():
    apprentice = Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Pender")
    labourer = Employee(EmployeeRole.PENDING_INSTALLER, "Labourer Bender")
    roster = Roster({apprentice, labourer})
    roster.scheduled["Tuesday"] = {labourer}

    labourers = roster.get_available_employees("Tuesday", EmployeeRole.LABOURER)
    pending_installers = roster.get_available_employees("Tuesday", EmployeeRole.PENDING_INSTALLER)
    assert len(labourers) == 0
    assert len(pending_installers) == 1


def test_schedule_employee_multiple_days():
    employees = {
        Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Flavian"),
    }
    roster = Roster(employees)

    monday_employee = roster.schedule_employee("Monday")
    thursday_employee = roster.schedule_employee("Thursday")

    assert monday_employee.name == "Installer Flavian"
    assert thursday_employee.name == "Installer Flavian"


def test_meets_worker_requirements():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.LABOURER, "Labourer Lily"),
        }
    )
    requirements = [EmployeeRole.CERTIFIED_INSTALLER]

    got = roster.meets_worker_requirements("Thursday", requirements)

    assert got is True


def test_does_not_have_enough_workers():
    roster = Roster(
        {
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Alfie"),
            Employee(EmployeeRole.LABOURER, "Labourer Lyra"),
        }
    )
    requirements = [
        EmployeeRole.PENDING_INSTALLER,
        EmployeeRole.PENDING_INSTALLER
    ]

    got = roster.meets_worker_requirements("Friday", requirements)

    assert got is False


def test_logical_or_requirement_success():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.LABOURER, "Labourer Lyra"),
        }
    )
    requirements = [
        EmployeeRole.CERTIFIED_INSTALLER,
        (EmployeeRole.LABOURER, EmployeeRole.PENDING_INSTALLER)
    ]

    got = roster.meets_worker_requirements("Monday", requirements)

    assert got is True


def test_logical_or_requirement_is_not_too_greedy():
    roster = Roster(
        {
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Andy"),
            Employee(EmployeeRole.LABOURER, "Labourer Lyra"),
        }
    )
    requirements = [
        (EmployeeRole.LABOURER, EmployeeRole.PENDING_INSTALLER),
        EmployeeRole.PENDING_INSTALLER
    ]

    got = roster.meets_worker_requirements("Monday", requirements)

    assert got is True


def test_requirements_with_logical_or_fails():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Labourer Lyra"),
        }
    )
    requirements = [
        EmployeeRole.CERTIFIED_INSTALLER,
        (EmployeeRole.LABOURER, EmployeeRole.PENDING_INSTALLER)
    ]

    got = roster.meets_worker_requirements("Monday", requirements)

    assert got is False


def test_requirements_any():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Andy"),
            Employee(EmployeeRole.LABOURER, "Labourer Lyra"),
        }
    )
    requirements = [EmployeeRole.ANY, EmployeeRole.ANY, EmployeeRole.ANY]

    got = roster.meets_worker_requirements("Monday", requirements)

    assert got is True


def test_final_unmet_requirement_fails():
    roster = Roster(
        {
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Zulu"),
            Employee(EmployeeRole.LABOURER, "Labourer Lennix"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Terry"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Larry"),
            Employee(EmployeeRole.LABOURER, "Labourer Lyra"),
            Employee(EmployeeRole.CERTIFIED_INSTALLER, "Installer Ian"),
            Employee(EmployeeRole.PENDING_INSTALLER, "Apprentice Mary"),
            Employee(EmployeeRole.LABOURER, "Labourer Lisa"),
        }
    )
    requirements = [
        EmployeeRole.CERTIFIED_INSTALLER,
        EmployeeRole.CERTIFIED_INSTALLER,
        (EmployeeRole.PENDING_INSTALLER,),
        (EmployeeRole.PENDING_INSTALLER, EmployeeRole.LABOURER),
        EmployeeRole.ANY, EmployeeRole.ANY, EmployeeRole.ANY,
        EmployeeRole.CERTIFIED_INSTALLER,
    ]

    got = roster.meets_worker_requirements("Tuesday", requirements)

    assert got is False
