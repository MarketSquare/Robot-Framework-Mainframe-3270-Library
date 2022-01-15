from invoke import task


@task
def lint_python(c):
    """Perform python code formatting with black, isort and flake8"""
    c.run("black ./tasks.py Mainframe3270/")
    c.run("isort ./tasks.py Mainframe3270/")
    c.run("flake8 ./tasks.py Mainframe3270/")


@task
def lint_robot(c):
    """Perform robot code formatting with robotidy"""
    c.run("robotidy tests/")


@task(lint_python, lint_robot)
def lint(c):
    """
    Perform code formatting for both robot and python code.

    Short option for `inv lint-python && inv lint-robot`.
    """
    pass
