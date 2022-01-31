from invoke import task


@task
def lint_python(c):
    """Perform python code formatting with black, isort and flake8"""
    c.run("black ./setup.py ./tasks.py Mainframe3270/ utest/")
    c.run("isort ./setup.py ./tasks.py Mainframe3270/ utest/")
    c.run("flake8 ./setup.py ./tasks.py Mainframe3270/ utest/")


@task
def lint_robot(c):
    """Perform robot code formatting with robotidy"""
    c.run("robotidy atest/")


@task(lint_python, lint_robot)
def lint(c):
    """
    Perform code formatting for both robot and python code.

    Short option for `inv lint-python && inv lint-robot`.
    """
    pass


@task
def utest(c):
    """Runs python unit tests"""
    c.run("pytest utest/")


@task
def atest(c):
    """Runs robot acceptance tests"""
    c.run("robot --loglevel DEBUG atest/")


@task(utest, atest)
def test(c):
    """Runs unit and acceptance tests.

    Short option for `inv utest && inv atest`.
    """
    pass
