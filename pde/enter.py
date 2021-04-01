# This python3 click subcommand enters a running pde container

import click
import logging
import os
import sys

@click.command("enter")
@click.option("-w", "--work-dir", default=None,
  help="The working directory in which to enter the container.")
@click.pass_context
def enter(ctx, work_dir) :
  """
  Enters a running pde container.
  """
  pCmd = "podman exec -it"
  if work_dir is not None :
    logging.info("Using the [{}] working directory".format(work_dir))
    pCmd = pCmd + " --workdir {}".format(work_dir)
  pCmd = pCmd + " {} {}".format(
    ctx.obj['pdeName'], ctx.obj['pde']['interactiveShell']
  )

  logging.info("using podman command:\n-----\n" + pCmd + "\n-----")
  click.echo("Entering {}".format(ctx.obj['pdeName']))
  click.echo("-------------------------------------------")
  sys.stdout.flush()
  os.system(pCmd)
  sys.stdout.flush()
  click.echo("-------------------------------------------")
  click.echo("Leaving {}".format(ctx.obj['pdeName']))
