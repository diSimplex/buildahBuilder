# This python3 click subcommand creates a new pde commons area

import click
import jinja2
import logging
import os
import shutil


def renderTemplate(ctx, fileName) :
  def j2_lookup_filter(value, tableName) :
    """
      Uses the filter provided value as a key to a result value in a dictionary.
    """
    if tableName not in ctx.obj :
      raise Exception("Lookup filter: There is no dictionary named {}".format(tableName))
      
    theTable = ctx.obj[tableName]

    if type(theTable) is not dict :
      raise Exception("Lookup filter: {} is not a dictionary".format(tableName))

    if value not in theTable :
      raise Exception("Lookup filter: The value [{}] is not in the dictionary {}".format(value, tableName))

    return theTable[value]

  tmplEnv = jinja2.Environment()
  tmplEnv.filters['lookup'] = j2_lookup_filter
  
  try: 
    with open(fileName, 'r') as inFile :
      template = tmplEnv.from_string(inFile.read())
    with open(os.path.join(ctx.obj['pdeDir'], fileName), 'w') as outFile :
      outFile.write(template.render(ctx.obj))
  except Exception as err:
    logging.error("Could not render the Jinja2 template [{}]".format(fileName))
    logging.error(err)

@click.command("create")
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
