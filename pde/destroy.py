# This python3 click subcommand destroys the commons area for a given pde

import click
import shutil

@click.command("destroy")
@click.option('-a', '--all', is_flag=True, default=False,
  help="Deletes ALL directories associated with the pde")
@click.option('-y', '--yes', is_flag=True, expose_value=True,
  help="Confirms that you want to delete this pde.",
  prompt="Are you sure you want to delete this pde?")
@click.pass_context
def destroy(ctx, all, yes) :
  """
  Remove the commons area for a given pde.
  """

#  if yes :
#    if all :
#      click.echo("Deleting {} (all)".format(ctx.obj['pdeName']))
#      shutil.rmtree(ctx.obj['pdeDir'], ignore_errors=True)
#    else:
#      click.echo("Deleting {} (workDir)".format(ctx.obj['pdeName']))
#      shutil.rmtree(ctx.obj['pdeWorkDir'], ignore_errors=True)
