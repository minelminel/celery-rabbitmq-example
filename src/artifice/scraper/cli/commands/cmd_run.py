import subprocess

import click


@click.command()
# @click.option('--test|--devel|--prod', default='--devel', help='Which runtime environment?')
@click.option('--env', type=click.Choice(['test', 'dev', 'prod']), help='Which runtime environment?')
@click.argument('env')
def cli(env):
    """
    Run the entire application.
    """
    cmd = 'echo \"Starting application...\nEnvironment: {}\"'.format(env.upper())
    return subprocess.call(cmd, shell=True)
