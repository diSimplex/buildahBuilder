# This python3 click subcommand runs a single cmd in a running pde container

import click
import logging
import os
import sys
import yaml
  
@click.command("run")
@click.option("-d", "--detached", is_flag=True,
  help="Run the command in a detached background.")
@click.option("-w", "--work-dir", default=None,
  help="The working directory in which to run the command.")
@click.argument("cmd_args", nargs=-1, required=True)
@click.pass_context
def run(ctx, detached, work_dir, cmd_args):
  """
  Runs a single command inside a running pde container.

  This subcommand uses (rootless) podman to run a single command inside an 
  existing pde container using the CMD_ARGS command line arguments. 

  NOTE: if your CMD_ARGS contain ``-`` or ``--`` options, then you will 
  need to use the ``--`` "option" after the run options and before the 
  CMD_ARGS. For example:

    pde cpDev run -- lua -v

  or

    pde cpDev run --work-dir /usr/local/src/lua -- /common/test

  where ``test`` is a shell script in the ~/common/pde/cpDev directory
  on the host (and the /common directory inside the container).

  """
  if cmd_args is None :
    click.echo("No command specified... nothting to do!")
    sys.exit(-1)
    
  cmdStr = " ".join(cmd_args)


  pCmd = "podman exec"
  
  if detached :
    logging.info("Running in detached background mode.")
    pCmd = pCmd + " --detach"
  else :
    pCmd = pCmd + " -it"

  if work_dir is not None :
    logging.info("Using the [{}] working directory".format(work_dir))
    pCmd = pCmd + " --workdir {}".format(work_dir)
    
  pCmd = pCmd + " {} {}".format(ctx.obj['pdeName'], cmdStr)
  
  logging.info("using podman command:\n-----\n" + pCmd + "\n-----")
  try:
    click.echo("Running    {}".format(ctx.obj['pdeName']))
    click.echo("Using cmd: [{}]".format(cmdStr))
    logging.info("using podmand command: \n-----\n" + pCmd + "\n-----")
    click.echo("\n---------------------------------------------------")
    sys.stdout.flush()
    os.system(pCmd)
    sys.stdout.flush()
    click.echo("---------------------------------------------------\n")
    click.echo("Finished.")
  except:
    pass
