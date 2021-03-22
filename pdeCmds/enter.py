# This python3 click subcommand enters a running pde container

import click
import logging
import os
import pdeCmds
import sys

@pdeCmds.cli.command()
@click.pass_context
def enter(ctx) :
  """
  Enters a running pde container.
  """
  shell = "bash"
  if 'shell' in ctx.obj['pde'] :
    shell = ctx.obj['pde']['shell']
  try:
    click.echo("Entering {}".format(ctx.obj['pdeName']))
    click.echo("-------------------------------------------")
    sys.stdout.flush()
    os.system("podman exec -it {} {} -l".format(ctx.obj['pdeName'], shell))
    sys.stdout.flush()
    click.echo("-------------------------------------------")
    click.echo("Leaving {}".format(ctx.obj['pdeName']))
  except :
    pass
