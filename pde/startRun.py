# This python3 click subcommand starts a pde container

import click
import logging
import os
import sys
import yaml

def compileCmd(ctx, workDir, cmdArgs):
  image = {}
  if 'image' in ctx.obj and ctx.obj['image'] :
    image = ctx.obj['image']
  else :
    logging.error("No image description found ... can not start pde!")
    sys.exit(-1)

  pde = {}
  if 'pde' in ctx.obj :
    pde = ctx.obj['pde']
  else :
    logging.error("No pde description found ... can not start pde!")
    sys.exit(-1)

  logging.info("(re)creating the commons directory")
  os.makedirs(ctx.obj['pdeDir'], exist_ok=True)

  ####################################################################
  # We start by fixing any magic parameters...
  #
  if 'user' not in pde :
    pde['user'] = 'root'

  if 'userDir' not in pde :
    if pde['user'] == 'root' :
      pde['userDir'] = '/root'
    else:
      pde['userDir'] = '/home/{}'.format(pde['user'])

  if workDir is not None :
    pde['workingDir'] = workDir

  runEnvs = {}
  if 'runEnvs' in pde :
    runEnvs.update( pde['runEnvs'] )
  # add in DISPLAY 
  display =  os.getenv('DISPLAY')
  if display :
    runEnvs['DISPLAY'] = display
  # add in SSH_AUTH_SOCK
  sshAuthSock     = os.getenv('SSH_AUTH_SOCK')
  sshAuthSockDir  = None
  sshAuthSockFile = None
  if sshAuthSock :
    runEnvs['SSH_AUTH_SOCK'] = sshAuthSock
    sshAuthSockDir  = os.path.dirname(sshAuthSock)
    sshAuthSockFile = os.path.basename(sshAuthSock)

  volumes = []
  if 'volumes' in pde :
    volumes = pde['volumes']
  volumes.append("{}:/common".format(ctx.obj['pdeDir']))
  hostSSHdir = os.path.expanduser('~/.ssh')
  if os.path.isdir(hostSSHdir) :
    volumes.append("{}:{}/.ssh:ro".format(hostSSHdir, pde['userDir']))
  if sshAuthSockDir :
    mappedSshAuthSockDir = None
    for aVolume in volumes :
      if sshAuthSockDir in aVolume :
        mappedSshAuthSockDir = aVolume.split(':')[1]
        break
    if mappedSshAuthSockDir :
      if sshAuthSockFile :
        logging.info("Mapping sshAuthSockDir to [{}]".format(mappedSshAuthSockDir))
        runEnvs['SSH_AUTH_SOCK'] = os.path.join(mappedSshAuthSockDir, sshAuthSockFile)
    else :
      logging.info("Adding sshAuthSockDir [{}]".format(sshAuthSockDir))
      volumes.append("{}:{}:ro".format(sshAuthSockDir, sshAuthSockDir))

  ####################################################################
  # Now that we have all of the magic parameters set...
  # we can build ``the``strings to be used in the run cmd string...
  
  theUser = "-u \"{}:{}\"".format(pde['user'], pde['user'])
  theWorkingDir = ""
  if 'workingDir' in pde :
    theWorkingDir = "-w \"{}\"".format(pde['workingDir'])
  
  theRunEnvs = ""
  for aRunEnvKey, aRunEnvValue in runEnvs.items() :
    theRunEnvs = theRunEnvs + " -e \"{}={}\"".format(aRunEnvKey, aRunEnvValue)

  theVolumes = ""
  for aVolume in volumes :
    theVolumes = theVolumes + " -v " + aVolume
    volParts = aVolume.split(':')
    if not os.path.exists(volParts[0]) :
      os.makedirs(volParts[0], exist_ok=True)

  theDevices = ""
  if 'devices' in pde :
    for aDeviceSpec in pde['devices'] :
      theDevices = theDevices + " --device={}".format(aDeviceSpec)
  
  theCapabilities = ""
  if 'capabilities' in pde :
    if 'add' in pde['capabilities'] :
      for aCapability in pde['capabilities']['add'] :
        theCapabilities = theCapabilities + " --cap-add {}".format(aCapability)
    if 'drop' in pde['capabilities'] :
      for aCapability in pde['capabilities']['drop'] :
        theCapabilities = theCapabilities + " --cap-drop {}".format(aCapability)

  thePorts = ""
  if 'ports' in pde :
    for aPortMap in pde['ports'] :
      thePorts = thePorts + " --publish={}".format(aPortMap)

  theHosts = ""
  if 'hosts' in pde :
    for aHostMap in pde['hosts'] :
      theHosts = theHosts + " --add-host {}".format(aHostMap)

  detachedStr = "--detach=true"
  cmdStr      = "sleep infinity"
  if cmdArgs is not None :
    detachedStr = "-it"
    cmdStr      = " ".join(cmdArgs)
    
  ####################################################################
  # We can now assemble the run cmd string...
  #
  cmd = """
podman run \
  {detachedStr} \
  {theVolumes} \
  {theRunEnvs} \
  {theUser} \
  {theWorkingDir} \
  {theDevices} \
  {theCapabilities} \
  {thePorts} \
  {theHosts} \
  --hostname {pdeName} \
  --name {pdeName} \
  {imageName} \
  {cmdStr}
""".rstrip().format(
    detachedStr     = detachedStr,
    theVolumes      = theVolumes,
    theRunEnvs      = theRunEnvs,
    theDevices      = theDevices,
    theCapabilities = theCapabilities,
    thePorts        = thePorts,
    theHosts        = theHosts,
    theUser         = theUser,
    theWorkingDir   = theWorkingDir,
    pdeName         = ctx.obj['pdeName'],
    imageName       = ctx.obj['image']['name'],
    cmdStr          = cmdStr
  )
  return cmd

@click.command("start")
@click.pass_context
def start(ctx):
  """
  Starts an existing pde container image in the background.

  This subcommand uses (rootless) podman to run a pde container image.

  It uses the ``pde.yaml`` file (in the "common" area for a given pde) to 
  describe how to run the pde container image. 

  This ``pde.yaml`` file and the associated "common" area are created by 
  the ``create`` subcommand. 

  The current values in ``pde.yaml`` file will be listed in the ``pde`` 
  configuration key which can be found by using the ``config`` subcommand. 

  """
  cmd = compileCmd(ctx, None, None)
  
  ####################################################################
  # Now do it!
  #
  click.echo("Starting {}".format(ctx.obj['pdeName']))
  logging.info("using podman command:\n-----" + cmd + "\n-----")
  os.system(cmd)

@click.command("run")
@click.option("-w", "--work-dir", default=None,
  help="The working directory in which to run the command.")
@click.argument("cmd_args", nargs=-1, required=True)
@click.pass_context
def run(ctx, work_dir, cmd_args):
  """
  Runs an existing pde container image using the CMD_ARGS command line arguments.

  This subcommand uses (rootless) podman to run a pde container image.

  It uses the ``pde.yaml`` file (in the "common" area for a given pde) to 
  describe how to run the pde container image. 

  This ``pde.yaml`` file and the associated "common" area are created by 
  the ``create`` subcommand. 

  The current values in ``pde.yaml`` file will be listed in the ``pde`` 
  configuration key which can be found by using the ``config`` subcommand.

  NOTE: if your CMD_ARGS contain ``-`` or ``--`` options, then you will 
  need to use the ``--`` "option" after the run options and before the 
  CMD_ARGS. For example:

    pde cpDev run -- lua -v

  or

    pde cpDev run --work-dir /usr/local/src/lua -- /common/test

  where ``test`` is a shell script in the ~/common/pde/cpDev directory
  on the host (and the /common directory inside the container).

  """
  cmd = compileCmd(ctx, work_dir, cmd_args)
  
  ####################################################################
  # Now do it!
  #
  click.echo("Running {}".format(ctx.obj['pdeName']))

  if work_dir is not None :
    logging.info("Using the [{}] working directory".format(work_dir))
    
  logging.info("using podman command:\n-----" + cmd + "\n-----")
  click.echo("\n---------------------------------------------------")
  os.system(cmd)
  click.echo("---------------------------------------------------\n")
  
  click.echo("Stopping {}".format(ctx.obj['pdeName']))
  os.system("podman container stop {}".format(ctx.obj['pdeName']))
  os.system("podman container rm {}".format(ctx.obj['pdeName']))

