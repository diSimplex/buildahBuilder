# This python3 click subcommand builds a pde container image

import click
import logging
import pdeCmds
import os

@pdeCmds.cli.command()
@click.pass_context
def build(ctx):
  """

  Build a pde container image.

  This subcommand uses cekit to build a podman conatiner image for a given 
  pde. 

  The cekit tool uses the ``image.yaml`` YAML file (in the "common" area 
  for a given pde) to describe how to buile a container. 

  This ``image.yaml`` file and the associated "common" area are created by 
  the ``create`` subcommand. 

  The current values in ``image.yaml`` file will be listed in the 
  ``image`` configuration key which can be found by using the ``config`` 
  subcommand. 

  """
  click.echo("Building {}".format(ctx.obj['pdeName']))

  logging.info("Changing directory to: [{}]".format(ctx.obj['pdeDir']))
  os.chdir(ctx.obj['pdeDir'])

  cmdParts = []
  cmdParts.append("cekit")
  if ctx.obj['verbose'] :
    cmdParts.append("-v")
  cmdParts.append("--descriptor")
  cmdParts.append(ctx.obj['imageYaml'])
  cmdParts.append("--config")
  cmdParts.append(ctx.obj['cekitConfig'])
  cmdParts.append("build")
  cmdParts.append("podman")
  cmd = " ".join(cmdParts)

  logging.info("running: [{}]".format(cmd))
  os.system(cmd)
