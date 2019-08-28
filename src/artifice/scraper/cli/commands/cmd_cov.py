import subprocess

import click


@click.command()
@click.argument('path', default='artifice')
def cli(path):
    """
    Run a test coverage report.
    """
    cmd = 'py.test --cov-report term-missing --cov {0}'.format(path)
    return subprocess.call(cmd, shell=True)
