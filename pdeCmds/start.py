# This python3 click subcommand starts a pde container

import click
import logging
import os
import pdeCmds
import sys
import yaml

@pdeCmds.cli.command()
@click.pass_context
def start(ctx):
  """
  Starts an existing pde container image.

  This subcommand uses (rootless) podman to run a pde container image.

  It uses the ``pde.yaml`` file (in the "common" area for a given pde) to 
  describe how to run the pde container image. 

  This ``pde.yaml`` file and the associated "common" area are created by 
  the ``create`` subcommand. 

  The current values in ``pde.yaml`` file will be listed in the ``pde`` 
  configuration key which can be found by using the ``config`` subcommand. 

  """
  
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

  theRunEnvs = ""
  runEnvs = {}
  runEnvs['DISPLAY'] = "unix:0.0"
  sshAuthSock    = os.getenv('SSH_AUTH_SOCK')
  sshAuthSockDir = None
  if sshAuthSock :
    runEnvs['SSH_AUTH_SOCK'] = sshAuthSock
    sshAuthSockDir = os.path.dirname(sshAuthSock)
  if 'runEnvs' in pde :
    runEnvs.update( pde['runEnvs'] )
  for aRunEnvKey, aRunEnvValue in runEnvs.items() :
    theRunEnvs = theRunEnvs + " -e \"{}={}\"".format(aRunEnvKey, aRunEnvValue)

  theVolumes = ""
  volumes = []
  if 'volumes' in pde :
    volumes = pde['volumes']
  xsock = "/tmp/.X11-unix"
  volumes.append("{}:{}".format(xsock, xsock))
  volumes.append("{}:/common".format(ctx.obj['pdeDir']))
  volumes.append("/home/dev/.ssh:/home/dev/.ssh:ro")
  volumeFound = False
  if sshAuthSockDir :
    for aVolume in volumes :
      if sshAuthSockDir in aVolume :
        volumeFound = True
        break
  if not volumeFound :
    logging.info("Adding sshAuthSockDir [{}]".format(sshAuthSockDir))
    volumes.append("{}:{}:ro".format(sshAuthSockDir, sshAuthSockDir))
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


  theHosts = ""
  if 'hosts' in pde :
    for aHostMap in pde['hosts'] :
      theHosts = theHosts + " --add-host {}".format(aHostMap)

  cmd = """
podman run -it \
  {theVolumes} \
  {theRunEnvs} \
  -u "dev:dev" \
  -w "/home/dev" \
  {theDevices} \
  {theCapabilities} \
  {theHosts} \
  --hostname {pdeName} \
  --name {pdeName} \
  {imageName}
""".rstrip().format(
    theVolumes      = theVolumes,
    theRunEnvs      = theRunEnvs,
    theDevices      = theDevices,
    theCapabilities = theCapabilities,
    theHosts        = theHosts,
    pdeName         = ctx.obj['pdeName'],
    imageName       = ctx.obj['image']['name']
   )

  click.echo("Running {}".format(ctx.obj['pdeName']))
  logging.info("running podman command:\n-----" + cmd + "\n-----")
  os.system(cmd)
