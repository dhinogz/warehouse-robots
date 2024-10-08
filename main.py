import uvicorn
import typer

cli = typer.Typer(no_args_is_help=True)


@cli.command("search")
def search():
    from models.search import robot_search

    robot_search()


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
