# This is the pde package

import click
import os
import yaml
import logging

########################################################################
# Handle configuration

defaultConfig = {
  'commonDir'   : "~/common",
  'configYaml'  : "config.yaml",
  'imageYaml'   : "image.yaml",
  'pdeYaml'     : "pde.yaml",
  'cekitConfig' : "cekit.ini",
  'verbose'     : False
}

def loadConfig(pdeName, configPath, verbose):

  # start with the default configuration (above)
  config = defaultConfig
  

  # Add the global configuration (if any)
  configPath = os.path.abspath(os.path.expanduser(configPath))
  try:
    globalConfigFile = open(configPath)
    globalConfig = yaml.safe_load(globalConfigFile)
    globalConfigFile.close()
    if globalConfig is not None : 
      config.update(globalConfig)
  except IOError:
    if verbose is not None and verbose :
      print("INFO: no global configuration file found: [{}]".format(configPath))

  # Now add in any local configuration 
  try:
    localConfigFile = open(config['configYaml'], 'r')
    localConfig = yaml.safe_load(localConfigFile)
    localConfigFile.close()
    if localConfig is not None : 
      config.update(localConfig)
  except IOError:
    if verbose is not None and verbose :
      print("INFO: no local configuration file found: [{}]".format(config['configYaml']))

  # Now add in command line argument/options
  if pdeName is not None :
    config['pdeName'] = pdeName

  if verbose is not None :
    config['verbose'] = verbose

  # Now sanitize any known configurable paths
  if configPath is not None :
    config['configPath'] = configPath
    config['configDir'] = os.path.dirname(configPath)
    
  if config['cekitConfig'][0] == "~" :
    config['cekitConfig'] = os.path.abspath(
        os.path.expanduser(config['cekitConfig']))

  if config['cekitConfig'][0] != "/" :
    config['cekitConfig'] = os.path.abspath(
        os.path.join(config['configDir'], config['cekitConfig']))

  config['commonDir'] = os.path.abspath(os.path.expanduser(config['commonDir']))
  config['pdeDir'] = os.path.join(config['commonDir'], "pde", config['pdeName'])

  config['curDir'] = os.path.abspath(os.getcwd())
  config['homeDir'] = os.path.expanduser("~")

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

    For details on all other configuration parameters type:

        pde -v help config
  """
  ctx.ensure_object(dict)
  ctx.obj = loadConfig(pde_name, config_file, verbose)
