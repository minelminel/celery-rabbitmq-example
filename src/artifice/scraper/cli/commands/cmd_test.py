import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.dirname(os.path.abspath(__name__)))
def cli(path):
    """
    Run tests with Pytest.
    """
    cmd = 'py.test {0}'.format(path)
    return subprocess.call(cmd, shell=True)
