import os
import matplotlib.pyplot as plt
from mesa.space import FloatCoordinate
import pyvisgraph as vg

ObstacleCorners = tuple[
    FloatCoordinate, FloatCoordinate, FloatCoordinate, FloatCoordinate
]


def read_pos(input: list[str]) -> list[FloatCoordinate]:
    x_coords = [float(x) for x in input[0].strip().split(",")]
    y_coords = [float(y) for y in input[1].strip().split(",")]
    return [(x, y) for x, y in zip(x_coords, y_coords)]


def read_obstacle(input: list[str]) -> ObstacleCorners:
    if len(input) != 2:
        raise Exception()

    x = [float(n) for n in input[0].strip().split(",")]
    y = [float(n) for n in input[1].strip().split(",")]

    return (
        (x[0], y[0]),
        (x[1], y[1]),
        (x[2], y[2]),
        (x[3], y[3]),
    )


def read_input() -> (
    tuple[list[FloatCoordinate], list[FloatCoordinate], list[ObstacleCorners]]
):
    robots: list[FloatCoordinate] = []
    goals: list[FloatCoordinate] = []
    obstacle_corners: list[ObstacleCorners] = []

    with os.scandir("inputs") as inputs:
        for i in inputs:
            with open(i.path, "r") as f:
                lines = f.readlines()

                if "Initial" in i.name:
                    robots = read_pos(lines)
                elif "Target" in i.name:
                    goals = read_pos(lines)
                elif "Obs" in i.name:
                    obs = read_obstacle(lines)
                    obstacle_corners.append(obs)

    return robots, goals, obstacle_corners


def add_buffer_to_polygon(
    polygon: list[FloatCoordinate], buffer: float
) -> list[tuple[float, float]]:
    from shapely import Polygon

    poly = Polygon(polygon)
    buffered_poly = poly.buffer(buffer)
    return list(buffered_poly.exterior.coords)[:-1]


def add_buffer_to_list_of_polygons(
    obstacle_corners: list[ObstacleCorners],
    buffer: float = 0.11,
) -> list:
    obstacles_polys = []
    buffered_obstacles = []
    for obs in obstacle_corners:
        poly = list(obs)
        obstacles_polys.append(poly)
        buffered_poly = add_buffer_to_polygon(poly, buffer)
        buffered_obstacles.append(buffered_poly)

    return buffered_obstacles


def add_path_to_graph(
    ax, g: vg.VisGraph, start: FloatCoordinate, goal: FloatCoordinate, color: str
) -> tuple[list, FloatCoordinate]:
    start_point = vg.Point(start[0], start[1])
    goal_point = vg.Point(goal[0], goal[1])
    path = g.shortest_path(start_point, goal_point)

    if path:
        x, y = zip(*[(p.x, p.y) for p in path])
        ax.plot(x, y, color=color, linewidth=2, label=f"Path ({color})")
    else:
        print(f"No path found for {color} robot")

    normalized_path = []
    for p in path:
        normalized_path.append((p.x, p.y))

    return normalized_path, goal


def write_path(path: list, filename: str):
    with open(f"output-{filename}", "w") as f:
        for p in path:
            f.write(f"{p[0]} {p[1]}\n")


def robot_search():
    robots, goals, obstacle_corners = read_input()

    obstacles_polys = []
    for obs in obstacle_corners:
        poly = list(obs)
        obstacles_polys.append(poly)

    buffered_obstacles = add_buffer_to_list_of_polygons(obstacle_corners)

    g = vg.VisGraph()
    g.build(
        [list(map(lambda p: vg.Point(p[0], p[1]), poly)) for poly in buffered_obstacles]
    )

    # Visualization
    _, ax = plt.subplots()

    # Plot original obstacles
    for poly in obstacles_polys:
        x, y = zip(*poly)
        ax.fill(x, y, alpha=0.3, color="gray")

    # Plot buffered obstacles
    for poly in buffered_obstacles:
        x, y = zip(*poly)
        ax.fill(x, y, alpha=0.5, color="purple")

    # Plot all goals in green
    goal_x, goal_y = zip(*goals)
    ax.scatter(goal_x, goal_y, color="green", s=100, label="Goals")

    # Plot robot 1 (blue) and robot 2 (red)
    ax.scatter(
        robots[0][0], robots[0][1], color="blue", s=150, label="Robot 1", marker="s"
    )
    ax.scatter(
        robots[1][0], robots[1][1], color="red", s=150, label="Robot 2", marker="s"
    )

    # Add paths for robot 1
    robot_blue_paths = []
    robot_blue = robots[0]
    robot_path, robot_blue = add_path_to_graph(ax, g, robot_blue, goals[0], "blue")
    robot_blue_paths.extend(robot_path)

    robot_path, robot_blue = add_path_to_graph(ax, g, robot_blue, goals[1], "blue")
    robot_blue_paths.extend(robot_path)

    robot_path, _ = add_path_to_graph(ax, g, robot_blue, goals[5], "blue")
    robot_blue_paths.extend(robot_path)

    robot_red_paths = []
    robot_red = robots[1]
    robot_path, robot_red = add_path_to_graph(ax, g, robot_red, goals[2], "red")
    robot_red_paths.extend(robot_path)

    robot_path, robot_red = add_path_to_graph(ax, g, robot_red, goals[3], "red")
    robot_red_paths.extend(robot_path)

    robot_path, _ = add_path_to_graph(ax, g, robot_red, goals[4], "red")
    robot_red_paths.extend(robot_path)

    write_path(robot_blue_paths, "blue_robot.txt")

    write_path(robot_red_paths, "red_robot.txt")

    ax.set_aspect("equal", "box")
    ax.legend()
    ax.set_title("Multi-Robot Path Planning with Obstacles")
    plt.show()
