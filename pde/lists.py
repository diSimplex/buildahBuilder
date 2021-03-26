# This python3 click subcommand stops a running pde container

import click
import os

@click.command("images")
@click.pass_context
def images(ctx) :
  """
  Lists all pde container images.
  """

  if 'image' in ctx.obj :
    image = ctx.obj['image']
    if 'name' in image :
      click.echo("Listing {} images".format(ctx.obj['pdeName']))
      os.system("podman images --filter reference={}".format(image['name']))

@click.command("containers")
@click.pass_context
def containers(ctx) :
  """
  Lists all pde containers.
  """

  click.echo("Listing {} containers".format(ctx.obj['pdeName']))
  os.system("podman container list --filter name={}".format(ctx.obj['pdeName']))
