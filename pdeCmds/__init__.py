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

def sanitizeFilePath(config, filePathKey, pathPrefix) :
  if config[filePathKey][0] == "~" :
    config[filePathKey] = os.path.abspath(
        os.path.expanduser(config[filePathKey]))

  if pathPrefix is not None :
    config[filePathKey] = os.path.join(pathPrefix, config[filePathKey])
    
  if config[filePathKey][0] != "/" :
    config[filePathKey] = os.path.abspath(config[filePathKey])

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
  except :
    if verbose is not None and verbose :
      print("INFO: no global configuration file found: [{}]".format(configPath))

  # Now add in any local configuration 
  try:
    localConfigFile = open(config['configYaml'], 'r')
    localConfig = yaml.safe_load(localConfigFile)
    localConfigFile.close()
    if localConfig is not None : 
      config.update(localConfig)
  except :
    if verbose is not None and verbose :
      print("INFO: no local configuration file found: [{}]".format(config['configYaml']))

  # Now add in command line argument/options
  if pdeName is not None :
    config['pdeName'] = pdeName
  else:
    print("ERROR: a pdeName must be specified!")
    os.exit(-1)

  if verbose is not None :
    config['verbose'] = verbose

  # Now sanitize any known configurable paths
  if configPath is not None :
    config['configPath'] = configPath
  else:
    print("ERROR: a configPath must be specified!")
    os.exit(-1)
  
  sanitizeFilePath(config, 'configPath', None)
  config['configDir'] = os.path.dirname(configPath)
  sanitizeFilePath(config, 'cekitConfig', config['configDir'])

  sanitizeFilePath(config, 'commonDir', None)
  config['pdeDir'] = os.path.join(config['commonDir'], "pde", config['pdeName'])
  sanitizeFilePath(config, 'imageYaml', config['pdeDir'])
  sanitizeFilePath(config, 'pdeYaml', config['pdeDir'])
  config['curDir'] = os.path.abspath(os.getcwd())
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

        pde <<pdeName>> config
  """
  ctx.ensure_object(dict)
  ctx.obj = loadConfig(pde_name, config_file, verbose)
