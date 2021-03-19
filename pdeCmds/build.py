#!/usr/bin/env python3

# This python3 module builds a pde container image

import click
import logging
import pdeCmds
import os

@pdeCmds.cli.command()
@click.pass_context
def build(ctx):
  """Builds a pde container image"""
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
