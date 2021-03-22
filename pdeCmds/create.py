# This python3 click subcommand creates a new pde commons area

import click
import jinja2
import logging
import os
import pdeCmds
import shutil

def renderTemplate(ctx, fileName) :
  try: 
    with open(fileName, 'r') as inFile :
      template = jinja2.Template(inFile.read())
    with open(os.path.join(ctx.obj['pdeDir'], fileName), 'w') as outFile :
      outFile.write(template.render(ctx.obj))
  except Exception as err:
    logging.error("Could not render the Jinja2 template [{}]".format(fileName))
    logging.error(err)

@pdeCmds.cli.command()
@click.pass_context
def create(ctx):
  """
  Creates a new pde enviroment.

  This command creates the `common` directory associated with this pde and 
  then expands the Readme.md, image.yaml and pde.yaml files using the 
  Jinja2 template engine, copying the results to the pde common directory. 

  The Jinja2 templates have access to all configuration values which will 
  be reported by using the `--verbose` command line switch. 

  You can use the local pde configuration file (by default, 'config.yaml' 
  in this directory) to provide additional key/value pairs for use by your 
  Jinja2 templates. 

  NOTE that any Jinja2 expressions used in YAML values MUST be wrapped in 
  quotes. 
    
  """
  click.echo("Creating {}".format(ctx.obj['pdeName']))

  logging.info("(re)creating the commons directory")
  os.makedirs(ctx.obj['pdeDir'], exist_ok=True)

  logging.info("expanding the Readme.md, image and pde yaml files using Jinja2")

  renderTemplate(ctx, "Readme.md")  
  renderTemplate(ctx, "image.yaml")
  renderTemplate(ctx, "pde.yaml")
