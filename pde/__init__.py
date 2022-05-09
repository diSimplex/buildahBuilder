# This is the pde package

import click
import logging
import os
import platform
import sys
import yaml

#######################################################################
# start by monkey patching click to allow aliased commands
# adapted from:
#   https://click.palletsprojects.com/en/8.1.x/advanced/#command-aliases
#
def aliased_get_command(self, ctx, cmd_name) :
  possibleCmd = self.orig_get_command(ctx, cmd_name)
  if possibleCmd is not None:
    return possibleCmd
  matches = [aCmd for aCmd in self.list_commands(ctx)
             if aCmd.startswith(cmd_name)]
  if not matches:
    return None
  elif len(matches) == 1:
    return self.orig_get_command(ctx, matches[0])
  ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

def aliased_resolve_command(self, ctx, args):
  # always return the full command name
  _, cmd, args = self.orig_resolve_command(ctx, args)
  return cmd.name, cmd, args

click.Group.orig_get_command = click.Group.get_command
click.Group.get_command = aliased_get_command

click.Group.orig_resolve_command = click.Group.resolve_command
click.Group.resolve_command = aliased_resolve_command

#######################################################################

import pde.build
import pde.config
import pde.create
import pde.destroy
import pde.enter
import pde.remove
import pde.run
import pde.start
import pde.stop
import pde.lists

########################################################################
# Handle configuration

defaultConfig = {
  'commonsDir'   : "~/GitTools/Commons",
  'configYaml'  : "config.yaml",
  'imageYaml'   : "image.yaml",
  'pdeYaml'     : "pde.yaml",
  'cekitConfig' : "cekit.ini",
  'verbose'     : False
}

def sanitizeFilePath(config, filePathKey, pathPrefix) :
  if config[filePathKey][0] == "~" :
    config[filePathKey] = os.path.abspath(
        os.path.expanduser(config[filePathKey]))

  if pathPrefix is not None :
    config[filePathKey] = os.path.join(pathPrefix, config[filePathKey])

  if config[filePathKey][0] != "/" :
    config[filePathKey] = os.path.abspath(config[filePathKey])

def loadConfig(pdeName, configPath, verbose):

  # Start with the default configuration (above)
  config = defaultConfig

  # Add the global configuration (if any)
  configPath = os.path.abspath(os.path.expanduser(configPath))
  try:
    with open(configPath) as globalConfigFile :
      globalConfig = yaml.safe_load(globalConfigFile)
      if globalConfig is not None : config.update(globalConfig)
  except :
    if verbose is not None and verbose :
      print("INFO: no global configuration file found: [{}]".format(configPath))

  # Now add in any local configuration
  try:
    with open(config['configYaml'], 'r') as localConfigFile :
      localConfig = yaml.safe_load(localConfigFile)
      if localConfig is not None : config.update(localConfig)
  except :
    if verbose is not None and verbose :
      print("INFO: no local configuration file found: [{}]".format(config['configYaml']))

  # Now add in command line argument/options
  if pdeName is not None :
    config['pdeName'] = pdeName.rstrip(os.sep)
  else:
    print("ERROR: a pdeName must be specified!")
    sys.exit(-1)

  if verbose is not None :
    config['verbose'] = verbose

  if configPath is not None :
    config['configPath'] = configPath
  else:
    print("ERROR: a configPath must be specified!")
    sys.exit(-1)

  # Now sanitize any known configurable paths
  sanitizeFilePath(config, 'configPath', None)
  config['configDir'] = os.path.dirname(configPath)
  sanitizeFilePath(config, 'cekitConfig', config['configDir'])

  sanitizeFilePath(config, 'commonsDir', None)
  config['pdeDir'] = os.path.join(config['commonsDir'], config['pdeName'])
  config['pdeWorkDir'] = os.path.join(config['pdeDir'], "pde")
  sanitizeFilePath(config, 'imageYaml', config['pdeWorkDir'])
  sanitizeFilePath(config, 'pdeYaml', config['pdeWorkDir'])
  config['curDir'] = os.path.join(os.path.abspath(os.getcwd()), config['pdeName'])
  config['homeDir'] = os.path.expanduser("~")

  # Now add in the image.yaml (if it exists)
  config['image'] = {}
  try:
    imageFile = open(config['imageYaml'], 'r')
    image = yaml.safe_load(imageFile)
    imageFile.close()
    if image is not None :
      config['image'] = image
  except IOError :
    if verbose is not None and verbose :
      print("INFO: could not load the image file: [{}]".format(config['imageYaml']))
  except Exception as e :
    if verbose is not None and verbose :
      print("INFO: could not load the image file: [{}]".format(config['imageYaml']))
      print("    > " + "\n    > ".join(str(e).split('\n')))
      print("  Did you remember to wrap all YAML values\n  with Jinja2 variables in quotes?")

  if 'run' not in config['image'] :
    config['image']['run'] = {}

  if 'user' not in config['image']['run'] :
    config['image']['run']['user'] = "root"

  if 'workdir' not in config['image']['run'] :
    config['image']['run']['workdir'] = "/commons"

  # Now add in the pde.yaml (if it exists)
  config['pde'] = {}
  try:
    pdeFile = open(config['pdeYaml'], 'r')
    pde = yaml.safe_load(pdeFile)
    pdeFile.close()
    if pde is not None :
      config['pde'] = pde
  except IOError :
    if verbose is not None and verbose :
      print("INFO: could not load the pde file: [{}]".format(config['pdeYaml']))
  except Exception as e :
    if verbose is not None and verbose :
      print("INFO: could not load the pde file: [{}]".format(config['pdeYaml']))
      print("\t" + "\n\t".join(str(e).split('\n')))
      print("\tDid you remember to wrap all YAML values\n\twith Jinja2 variables in quotes?")

  if 'shell' not in config['pde'] :
    if verbose is not None and verbose:
      print("INFO: setting shell to bash")
    config['pde']['shell'] = os.path.join("/", "bin", "bash")

  if 'shellrc' not in config['pde'] :
    if verbose is not None and verbose:
      print("INFO: setting shellrc to .bashrc")
    config['pde']['shellrc'] = os.path.join(
      config['image']['run']['workdir'],
      ".bashrc"
    )

  if 'interactiveShell' not in config['pde'] :
    if verbose is not None and verbose:
      print("INFO: setting interactive shell to bash")
    config['pde']['interactiveShell'] = os.path.join("/", "bin", "bash")

  # Now add in platform parameters
  thePlatform = {}
  thePlatform['system']    = platform.system()
  thePlatform['node']      = platform.node()
  thePlatform['release']   = platform.release()
  thePlatform['version']   = platform.version()
  thePlatform['machine']   = platform.machine()
  thePlatform['processor'] = platform.processor()
  config['platform']       = thePlatform

  # Setup logging
  if config['verbose'] :
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(levelname)s: %(message)s')

  # Let us see the loaded configuration if we are running --verbose
  logging.info("configuration:\n------\n" + yaml.dump(config) + "------\n")

  return config

########################################################################
# Now deal with click commands

@click.group()
@click.option("-v", "--verbose",
  help="Provide more diagnostic output.",
  default=False, is_flag=True)
@click.option("--config", "config_file",
  help="The path to the global pde configuration file.",
  default="~/.config/pde/config.yaml", show_default=True)
@click.argument('pde_name')
@click.pass_context
def cli(ctx, pde_name, config_file, verbose):
  """
    PDE_NAME is the name of the pde container on which subsequent commands will work.

    The pde subcommands (listed below) come in a number of pairs:

      config : used to view the configuration parameters as seen by pde,

      create/destroy : used to manage the "commons" area as well as image and pde descriptions,

      build/remove : used to manage the podman images used by a running container,

      start/stop : used to manage the running container used for development,

      enter : used to enter an already running conainter using the configured shell [default=bash] (this command may be used multiple times).

      run : used to run a single command in an already running conainter.

    For details on all other configuration parameters type:

        pde <<pdeName>> config
  """
  ctx.ensure_object(dict)
  ctx.obj = loadConfig(pde_name, config_file, verbose)

cli.add_command(pde.build.build)
cli.add_command(pde.config.config)
cli.add_command(pde.create.create)
cli.add_command(pde.destroy.destroy)
cli.add_command(pde.enter.enter)
cli.add_command(pde.lists.images)
cli.add_command(pde.lists.containers)
cli.add_command(pde.remove.remove)
cli.add_command(pde.run.run)
cli.add_command(pde.start.start)
cli.add_command(pde.stop.stop)
