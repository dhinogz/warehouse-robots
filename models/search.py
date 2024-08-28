from dataclasses import dataclass
import heapq
import random
from typing import List, Tuple, Optional
import logging

import mesa
from mesa.datacollection import DataCollector
from mesa.space import Coordinate, FloatCoordinate, NetworkCoordinate

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@dataclass
class Robot:
    pos_x: int
    pos_y: int


@dataclass
class Goal:
    pos_x: float
    pos_y: float


@dataclass
class Obstacle:
    corner_0: float
    corner_1: float
    corner_2: float
    corner_3: float


class ObstacleCell(mesa.Agent):
    """Represents an obstacle in the grid."""


class GoalCell(mesa.Agent):
    """Represents a goal in the grid."""


class RobotAgent(mesa.Agent):
    """Agent that finds paths to goals."""

    def __init__(self, unique_id: int, model):
        super().__init__(unique_id, model)
        self.path: List[Tuple[int, int]] = []

    def step(self):
        """Perform a single step of the agent."""
        pass
        # if not self.path:
        #     self.model.set_new_path(self)
        #
        # if self.path:
        #     next_pos = self.path.pop(0)
        #     self.model.grid.move_agent(self, next_pos)
        #     print(f"moving agent to {next_pos}")
        #
        #     cell_contents = self.model.grid.get_cell_list_contents([next_pos])
        #     for agent in cell_contents:
        #         if isinstance(agent, GoalCell):
        #             print(f"Found goal: {agent.unique_id}")
        #             self.model.remove_goal(agent)
        #             self.model.set_new_path()
        #             break
        #


SCALE_VALUE = 100


class PathfindingModel(mesa.Model):
    """Model for pathfinding simulation."""

    def __init__(
        self,
        width: int,
        height: int,
        robots: list[Robot],
        goals: list[Goal],
        obstacles: list[Obstacle],
    ):
        super().__init__()
        self.random = random
        self.schedule = mesa.time.SimultaneousActivation(self)

        self.grid = mesa.space.SingleGrid(width, height, True)

        self.width = width
        self.height = height

        self.robots = robots
        self.goals = goals
        self.obstacles = obstacles

        self.robot_agents: list[RobotAgent] = []
        self.goal_cells: list[GoalCell] = []

        self.logger = logging.getLogger(__name__)

        self._place_robots()
        self._place_goals()
        # self._place_obstacles()

        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"Remaining Goals": "num_goals"},
        )

    def set_new_path(self, robot_agent: RobotAgent):
        """Set a new path for the pathfinding agent."""
        if self.goal_cells:
            if robot_agent.pos is not FloatCoordinate:
                self.logger.error("No pos for robot agent")
                return
            start = (robot_agent.pos[0], robot_agent.pos[1])
            goal = self.random.choice(self.goals)
            new_path = self.a_star(start, (self.goals.pos_x, goal.pos_y))
            if new_path:
                self.robot_agents[0].path = new_path
            else:
                print(f"No path found to goal at {goal}. Choosing a new goal.")
                self.goals.remove(goal)
                self.set_new_path(robot_agent)
        else:
            self.running = False
            print("All goals have been found. Simulation complete.")

    def _place_robots(self):
        for i, r in enumerate(self.robots):
            robot_agent = RobotAgent(i, self)
            pos: Coordinate = (r.pos_x, r.pos_y)

            self.grid.place_agent(robot_agent, pos)
            self.robot_agents.append(robot_agent)
            self.schedule.add(robot_agent)

            self.set_new_path(robot_agent)

    def _place_goals(self):
        for i, g in enumerate(self.goals):
            goal_cell = GoalCell(i, self)
            pos: Coordinate = (
                self._scale_to_mesa(g.pos_x),
                self._scale_to_mesa(g.pos_y),
            )

            self.grid.place_agent(goal_cell, pos)
            self.goal_cells.append(goal_cell)

    def _place_obstacles(self):
        # TODO: calculate an obstacle that will take up n amount of grids. Each grid will have an obstacle cell
        for i, o in enumerate(self.obstacles):
            _ = o.corner_0
            # and so on...
            obstacle = ObstacleCell(i, self)
            x: int = 1
            y: int = 2
            pos = (x, y)
            self.grid.place_agent(obstacle, pos)

    def step(self):
        """Perform a single step of the model."""
        self.schedule.step()
        self.datacollector.collect(self)

        if not self.goals:
            self.running = False
            print("All goals have been found")

    def remove_goal(self, goal_cell: GoalCell):
        """Remove a goal from the model."""
        pass
        # self.goals.remove(goal_agent.pos)
        # self.grid.remove_agent(goal_agent)
        # self.num_goals -= 1
        # self.logger.info(f"Goal found! Remaining goals: {self.num_goals}")

    def a_star(
        self, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """Implement the A* algorithm for pathfinding."""

        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def get_neighbors(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
            neighbors = []
            for dx, dy in DIRECTIONS:
                next_pos = (pos[0] + dx, pos[1] + dy)
                if self.grid.out_of_bounds(next_pos):
                    continue
                cell_contents = self.grid.get_cell_list_contents([next_pos])
                if any(isinstance(agent, ObstacleCell) for agent in cell_contents):
                    continue
                neighbors.append(next_pos)
            return neighbors

        heap = [(0, start)]
        came_from = {}
        cost_so_far = {start: 0}
        closed_set = set()

        while heap:
            _, current = heapq.heappop(heap)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            closed_set.add(current)

            for next_pos in get_neighbors(current):
                if next_pos in closed_set:
                    continue

                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(heap, (priority, next_pos))
                    came_from[next_pos] = current

        return None


def run_model(
    width: int,
    height: int,
    robots: list[Robot],
    goals: list[Goal],
    obstacles: list[Obstacle],
):
    """Run the pathfinding model."""
    model = PathfindingModel(width, height, robots, goals, obstacles)
    while model.running:
        model.step()
