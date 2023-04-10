from invoke import task


@task
def lint_python(c):
    """Perform python code formatting with black, isort and flake8."""
    c.run("black ./setup.py ./tasks.py Mainframe3270/ utest/")
    c.run("isort ./setup.py ./tasks.py Mainframe3270/ utest/")
    c.run("flake8 ./setup.py ./tasks.py Mainframe3270/ utest/")
    c.run("mypy ./setup.py ./tasks.py Mainframe3270/")


@task
def lint_robot(c):
    """Perform robot code formatting with robotidy."""
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
    """Runs python unit tests."""
    c.run("pytest utest/")


@task
def atest(c):
    """Runs robot acceptance tests."""
    c.run("robot --loglevel DEBUG atest/")


@task(utest, atest)
def test(c):
    """Runs unit and acceptance tests.

    Short option for `inv utest && inv atest`.
    """
    pass


@task
def build_release(c):
    """Build a source and binary distro for the project.
    Manual steps to take before running this command is to change the version
    in `Mainframe3270/version.py`.
    """
    c.run("python -m build")


@task
def kw_docs(c):
    """Generates the keyword documentation with libdoc.

    Creates a html and a xml file and places them under doc/.
    """
    c.run("python -m robot.libdoc Mainframe3270/ doc/Mainframe3270.html")
    c.run("python -m robot.libdoc Mainframe3270/ doc/Mainframe3270.xml")
