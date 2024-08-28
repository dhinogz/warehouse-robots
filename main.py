import os
import uvicorn

import typer

cli = typer.Typer(no_args_is_help=True)


@cli.command("model")
def run_model():
    from models.search import run_model, Robot, Goal, Obstacle

    robots: list[Robot] = []
    goals: list[Goal] = []
    obstacles: list[Obstacle] = []

    with os.scandir("inputs") as inputs:
        for i in inputs:
            with open(i.path, "r") as f:
                if "Initial" in i.name:
                    # process initial positions
                    lines = f.readlines()
                    x_coords = [float(x) for x in lines[0].strip().split(",")]
                    y_coords = [float(y) for y in lines[1].strip().split(",")]
                    robots = [Robot(x, y) for x, y in zip(x_coords, y_coords)]

                elif "Target" in i.name:
                    # process target positions
                    lines = f.readlines()
                    x_coords = [float(x) for x in lines[0].strip().split(",")]
                    y_coords = [float(y) for y in lines[1].strip().split(",")]
                    goals = [Goal(x, y) for x, y in zip(x_coords, y_coords)]

                elif "Obs" in i.name:
                    lines = f.readlines()
                    for line in lines:
                        coords = [float(coord) for coord in line.strip().split(",")]
                        obstacle = Obstacle(coords[0], coords[1], coords[2], coords[3])
                        obstacles.append(obstacle)

    width: int = 6
    height: int = 4
    run_model(width, height, robots, goals, obstacles)


@cli.command()
def help():
    """
    Help info
    """
    typer.echo("Help for coolify CLI")


@cli.command("serve")
def serve_api(
    host: str = "0.0.0.0", port: int = 8000, workers: int = 3, is_dev: bool = True
):
    uvicorn.run(
        "api:get_api",
        workers=workers,
        host=host,
        port=port,
        reload=is_dev,
    )


if __name__ == "__main__":
    cli()
