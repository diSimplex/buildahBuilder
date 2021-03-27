# This python3 click subcommand starts a pde container

import click
import logging
import os
import sys
import yaml

@click.command("start")
@click.pass_context
def start(ctx):
  """
  (re)Starts an existing pde container in the background.

  """
  click.echo("Starting {}".format(ctx.obj['pdeName']))
  os.system("podman container start {}".format(ctx.obj['pdeName']))
