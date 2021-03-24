# This python3 click subcommand stops a running pde container

import click
import os

@click.command("stop")
@click.option('-y', '--yes', is_flag=True, expose_value=True,
  help="Confirms that you want to stop this container.",
  prompt='Are you sure you want to stop the container?')
@click.pass_context
def stop(ctx, yes) :
  """
  Stops a running pde container.
  """

  if yes: 
    try:
      click.echo("Stopping {}".format(ctx.obj['pdeName']))
      os.system("podman container stop {}".format(ctx.obj['pdeName']))
      os.system("podman container rm {}".format(ctx.obj['pdeName']))
    except:
      pass
