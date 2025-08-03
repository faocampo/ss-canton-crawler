"""Command line interface for the crawler package."""

import click


@click.command()
@click.option("--test", is_flag=True, help="Run the crawler in test mode.")
@click.option(
    "--threads",
    default=1,
    type=int,
    show_default=True,
    help="Number of threads to use",
)
def main(test: bool, threads: int) -> None:
    """Entry point for the crawler CLI."""
    if test:
        click.echo(f"Running in test mode with {threads} threads.")
    else:
        click.echo(f"Running with {threads} threads.")


if __name__ == "__main__":
    main()
