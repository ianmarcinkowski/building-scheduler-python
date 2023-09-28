""" Building Scheduler """

from building_scheduler.building import Building
from building_scheduler.roster import (
    Employee,
    Roster,
)


class DailyBuildingSchedule:
    def __init__(self, building: Building, employees: list[Employee]):
        self.building = building
        self.employees = employees

    def __repr__(self):
        return f"{self.building}: {', '.join(e.name for e in self.employees)}"


class BuildingScheduler:
    def __init__(self, buildings: list[Building], employee_roster: Roster):
        self.buildings = buildings
        self.roster = employee_roster
        self.daily_schedules = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }
        self.scheduled_buildings = []

    def generate_weekly_schedule(self):
        """
        Generate a whole week schedule.

        Intentionally departing from spec `schedule(buildings, employees)` signature
        to meet with most local language.  Having a separate method for getting a
        daily schedule implies the existance of a weekly schedule.

        This class will be used externally by an application which will fit with
        the original spec function signature.
        """
        for day in self.daily_schedules.keys():
            daily_schedule = self.generate_daily_schedule(day)
            self.daily_schedules[day] = daily_schedule

    def generate_daily_schedule(self, day: str) -> list[DailyBuildingSchedule]:
        building_schedules = []
        for building in self.remaining_buildings:
            can_schedule_building = self.roster.meets_worker_requirements(
                day, building.worker_requirements
            )
            if can_schedule_building:
                scheduled_employees = []
                for role in building.worker_requirements:
                    scheduled_employees.append(self.roster.schedule_employee(day, role))
                building_schedules.append(
                    DailyBuildingSchedule(building, scheduled_employees)
                )
                self.scheduled_buildings.append(building)
        return building_schedules

    @property
    def remaining_buildings(self):
        return list(
            filter(
                lambda building: building not in self.scheduled_buildings,
                self.buildings,
            )
        )
