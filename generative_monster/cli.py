import typer

from generative_monster.core import Monster 

app = typer.Typer()


@app.command()
def create():
    m = Monster()
    m.create()


@app.command()
def create_from_prompt(prompt: str, style: str):
    m = Monster()
    m.create_from_prompt(prompt, style)


if __name__ == "__main__":
    app()