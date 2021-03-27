# This python3 click subcommand removes any images associated with a pde

import click
import logging
import os

@click.command("remove")
@click.option('-y', '--yes', is_flag=True, expose_value=True, 
  help="Confirms that you want to remove this container image.",
  prompt="Are you sure you want to remove the container image?")
@click.pass_context
def remove(ctx, yes) :
  """
  Removes a pde container image.
  """

  if ctx.obj['image']['name'] and yes :
    try:
      click.echo("Removing the {} container".format(ctx.obj['pdeName']))
      os.system("podman container stop {}".format(ctx.obj['pdeName']))
      os.system("podman container rm {}".format(ctx.obj['pdeName']))
    except:
      logging.error("Could not remove the {} container".format(ctx.obj['pdeName']))
      logging.error(e)
    try:
      click.echo("Removing the {} container image (version)".format(ctx.obj['pdeName']))
      os.system("podman image rm {}:{}".format(ctx.obj['image']['name'], ctx.obj['image']['version']))
    except Exception as e :
      logging.error("Could not remove the {} (version) container image".format(ctx.obj['pdeName']))
      logging.error(e)
    try:
      click.echo("Removing the {} container image (latest)".format(ctx.obj['pdeName']))
      os.system("podman image rm {}:latest".format(ctx.obj['image']['name']))
    except Exception as e :
      logging.error("Could not remove the {} (latest) container image".format(ctx.obj['pdeName']))
      logging.error(e)
