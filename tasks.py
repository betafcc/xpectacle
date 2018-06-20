from invoke import task


SRC_DIR = 'xpectacle'


@task
def lint(c):
    c.run('python -m flake8')


@task
def typecheck(c):
    c.run(f'python -m mypy {SRC_DIR}')


@task(lint, typecheck)
def validate(c):
    pass
