from invoke import task


def simple_task(name: str, command: str):
    def caller(c):
        c.run(f"echo running {name}")
        c.run(command)

    return task(caller, name=name)


black = simple_task("black", "black .")
isort = simple_task("isort", "isort .")
format = simple_task("format", "inv black isort")

flake8 = simple_task("flake8", "flake8")
mypy = simple_task("mypy", "mypy .")
lint = simple_task("lint", "inv flake8 mypy")
test = simple_task("test", "pytest --cov")
