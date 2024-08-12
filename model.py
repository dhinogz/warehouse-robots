from mesa.model import Model
from mesa.agent import Agent
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation

from enum import Enum


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class ObstacleCell(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)


class GoalCell(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)


class Package(Agent):
    def __init__(self, unique_id: int, model: Model, sku: str) -> None:
        super().__init__(unique_id, model)
        self.sku = sku


class RobotType(Enum):
    LOAD = 1
    UNLOAD = 2


class RobotState(Enum):
    LOOKING = 1
    PICKING = 2
    TRANSPORTING = 3


class RobotAgent(Agent):
    def __init__(self, unique_id, model, robot_type: RobotType):
        super().__init__(unique_id, model)
        self.robot_type = robot_type
        self.path = []

    def step(self):
        """
        1. Check if robot still has battery
        2. Check robot state
        3. Check if robot is on a current path and act accordinglyi
        """
        print("agent stepping")

    def advance(self):
        """
        Called after step method
        """
        print("agent advancing")


class WarehouseModel(Model):
    def __init__(self, m: int, n: int):
        super().__init__()

        self.grid = SingleGrid(m, n, False)
        self.schedule = SimultaneousActivation(self)

    def step(self):
        print("model stepping")
        self.schedule.step()
