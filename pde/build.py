# This python3 click subcommand builds a pde container image

import click
import logging
import os
import sys

##########################################################################
def buildCmd(ctx, override):
  logging.info("Changing directory to: [{}]".format(ctx.obj['pdeDir']))
  os.chdir(ctx.obj['pdeWorkDir'])

  cmdParts = []
  cmdParts.append("cekit")
  if ctx.obj['verbose'] :
    cmdParts.append("-v")
  cmdParts.append("--descriptor")
  cmdParts.append(ctx.obj['imageYaml'])
  cmdParts.append("--config")
  cmdParts.append(ctx.obj['cekitConfig'])
  cmdParts.append("build")

  if override is not None :
    cmdParts.append("--overrides-file")
    cmdParts.append(override)
  else:
    override = "override-{}.yaml".format(ctx.obj['platform']['machine'])
    if os.path.isfile(override) :
      cmdParts.append("--overrides-file")
      cmdParts.append(override)
     
  cmdParts.append("podman")
  cmd = " ".join(cmdParts)
  return cmd
  
##########################################################################
def startCmd(ctx):
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
  volumes.append("{}:/commons".format(ctx.obj['pdeDir']))
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

@click.command()
@click.option("-o", "--override", default=None,
  help="Specify an override file to be used during the build.")
@click.pass_context
def build(ctx, override):
  """

  Build and run a pde container image.

  This subcommand uses cekit to build a podman conatiner image for a given 
  pde. 

  The cekit tool uses the ``image.yaml`` YAML file (in the "commons" area 
  for a given pde) to describe how to buile a container. 

  This ``image.yaml`` file and the associated "commons" area are created by 
  the ``create`` subcommand. 

  The current values in ``image.yaml`` file will be listed in the 
  ``image`` configuration key which can be found by using the ``config`` 
  subcommand. 

  If the ``--override`` option is not specified but the pde working 
  directory contains a file named ``override-<<machine>>.yaml`` (where 
  ``<machine>>`` is the result of the Python ``platform.machine()`` 
  method), then this file is automatically used as an override file. 

  This subcommand the uses (rootless) podman to run a pde container in the 
  background. 

  It uses the ``pde.yaml`` file (in the "commons" area for a given pde) to 
  describe how to run the pde container image. 

  This ``pde.yaml`` file and the associated "commons" area are created by 
  the ``create`` subcommand. 

  The current values in ``pde.yaml`` file will be listed in the ``pde`` 
  configuration key which can be found by using the ``config`` subcommand. 

  """
  
  ####################################################################
  # Build the new image!
  #
  click.echo("Building {}".format(ctx.obj['pdeName']))

  cmd = buildCmd(ctx, override)
  logging.info("using the cekit command:\n-----\n" + cmd + "\n-----")
  click.echo("------------------------------------------------------------")
  sys.stdout.flush()
  result = os.system(cmd)
  sys.stdout.flush()
  click.echo("------------------------------------------------------------")
  if result != 0 :
    click.echo("Building {} FAILED!".format(ctx.obj['pdeName']))
    sys.exit(-1)
  
  ####################################################################
  # Start the container using the new image!
  #
  cmd = startCmd(ctx)
  click.echo("Starting {}".format(ctx.obj['pdeName']))
  logging.info("using podman command:\n-----\n" + cmd + "\n-----")
  click.echo("------------------------------------------------------------")
  sys.stdout.flush()
  os.system(cmd)
  sys.stdout.flush()
  click.echo("------------------------------------------------------------")

  ####################################################################
  # Run the finalization scripts
  #
  pCmd = "podman exec -it"
  
  shell = os.path.join("/", "bin", "bash")
  if 'shell' in ctx.obj['pde'] :
    shell = ctx.obj['pde']['shell']

  shellrc = os.path.join(ctx.obj['homeDir'], ".bashrc")
  if 'shellrc' in ctx.obj['pde'] :
    shellrc = ctx.obj['pde']['shellrc']
    
  pCmd = pCmd + " {} {} --login --rcfile {} -c \"{}\"".format(ctx.obj['pdeName'], shell, shellrc, cmdStr)
 
  click.echo("Finalizing {}".format(ctx.obj['pdeName']))
  logging.info("using podman command:\n-----\n" + cmd + "\n-----")
  click.echo("------------------------------------------------------------")
  sys.stdout.flush()
  os.system(cmd)
  sys.stdout.flush()
  click.echo("------------------------------------------------------------")
  
  ####################################################################
  # Stop the container until we want to use it...
  #
  os.system("podman container stop {}".format(ctx.obj['pdeName']))
