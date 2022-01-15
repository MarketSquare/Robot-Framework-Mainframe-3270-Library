from invoke import task


@task
def lint_python(c):
    """Perform code formatting with black, isort and flake8"""
    c.run("black ./tasks.py Mainframe3270/")
    c.run("isort ./tasks.py Mainframe3270/")
    c.run("flake8 ./tasks.py Mainframe3270/")
