from mesa.model import Model
from mesa.agent import Agent
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation


class ObstacleCell(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class GoalCell(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """
        A* solution for an agent looking for goal cell
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
