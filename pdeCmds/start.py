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
  if 'image' in ctx.obj :
    image = ctx.obj['image']
  else :
    logger.error("No image description found ... can not start pde!")
    os.exit(-1)

  pde = {}
  if 'pde' in ctx.obj :
    pde = ctx.obj['pde']
  else :
    logger.error("No pde description found ... can not start pde!")
    os.exit(-1)

  xsock = "/tmp/.X11-unix"

  logging.info("(re)creating the commons directory")
  os.makedirs(ctx.obj['pdeDir'], exist_ok=True)

  theVolumes = ""
  volumes = []
  if 'volumes' in pde :
    volumes = pde['volumes']
  volumes.append("{}:{}".format(xsock, xsock))
  volumes.append("{}:/common".format(ctx.obj['pdeDir']))
  volumes.append("/home/dev/.ssh:/home/dev/.ssh:ro")
  volumes.append("{}:/tmp/ssh-auth-sock:ro".format(os.getenv('SSH_AUTH_SOCK')))
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

  theRunEnvs = ""
  runEnvs = {}
  if 'runEnvs' in pde :
    runEnvs = pde['runEnvs']
  runEnvs['DISPLAY']       = "unix:0.0"
  runEnvs['SSH_AUTH_SOCK'] = "/tmp/ssh-auth-sock"
  for aRunEnvKey, aRunEnvValue in runEnvs.items() :
    theRunEnvs = theRunEnvs + " -e \"{}={}\"".format(aRunEnvKey, aRunEnvValue)

  cmd = """
podman run -it \
  {theVolumes} \
  {theRunEnvs} \
  -u "dev:dev" \
  -w "/home/dev" \
  {theDevices} \
  {theCapabilities} \
  --add-host nn01:10.0.0.1 \
  --add-host git.perceptisys.co.uk:10.0.0.1 \
  --hostname {pdeName} \
  --name {pdeName} \
  {imageName}
""".rstrip().format(
    theVolumes      = theVolumes,
    theRunEnvs      = theRunEnvs,
    theDevices      = theDevices,
    theCapabilities = theCapabilities,
    pdeName         = ctx.obj['pdeName'],
    imageName       = ctx.obj['image']['name']
   )

  logging.info("running podman command:\n-----" + cmd + "\n-----")
  #os.system(cmd)
