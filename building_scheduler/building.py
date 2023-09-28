""" Building """

from abc import ABCMeta, abstractmethod
from building_scheduler.roster import EmployeeRole


class Building(metaclass=ABCMeta):
    @property
    @abstractmethod
    def worker_requirements(self):
        pass


class SingleStoreyHome(Building):
    @property
    def worker_requirements(self):
        return [EmployeeRole.CERTIFIED_INSTALLER]

    def __repr__(self):
        return "Single Storey Home"


class TwoStoreyHome(Building):
    @property
    def worker_requirements(self):
        return [
            EmployeeRole.CERTIFIED_INSTALLER,
            (EmployeeRole.LABOURER, EmployeeRole.PENDING_INSTALLER),
        ]

    def __repr__(self):
        return "Two Storey Home"


class CommercialBuilding(Building):
    @property
    def worker_requirements(self):
        return [
            EmployeeRole.CERTIFIED_INSTALLER,
            EmployeeRole.CERTIFIED_INSTALLER,
            EmployeeRole.PENDING_INSTALLER,
            EmployeeRole.PENDING_INSTALLER,
            EmployeeRole.ANY,
            EmployeeRole.ANY,
            EmployeeRole.ANY,
            EmployeeRole.ANY,
        ]

    def __repr__(self):
        return "Commercial Building"
