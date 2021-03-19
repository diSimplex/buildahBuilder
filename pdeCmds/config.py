#!/usr/bin/env python3

# This python3 script starts a pde container

import click
import pdeCmds
  
@pdeCmds.cli.command()
@click.pass_context
def config(ctx):
  """More details about the various configuration options"""
  click.echo("""
The following configuration options can be specified in the global YAML 
configuraiton file.

This global configuration file is by default located in the file 

        ~/.config/pde/config.yaml

however you can use the `--config` option on the command line to specify a 
different path. 

The configuration options which can be over-ridden on the command line 
have their command line switches listed in brackets. 

--------------------------------------------------------------------------

commonDir:

    The path to the common directories mounted inside each pde container 
    as `/common`. This path is as it will be found on the host machine, 
    and may be either absolute or relative to the user's home directory 
    (~/common). 

imageYaml:

    The name of the image.yaml file used by cekit to describe how to build 
    the pde container image. 
    
pdeYaml:

    The name of the pde.yaml file used by pde to describe how to run a pde 
    container image. 

cekitConfig: 

    The name of the global INI configuration as used by our use of cekit. 
    If this option does not begin with a '/', then it assumed to be a path 
    relative to the configPath directory. 
        
verbose: (-v, --verbose)

    A boolean which specifies if additional working details should be 
    reported on the standard output. 
  """)
