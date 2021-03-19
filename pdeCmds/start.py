#!/usr/bin/env python3

# This python3 script starts a pde container

import click
import yaml
import sys
import pdeCmds

@pdeCmds.cli.command()
@click.pass_context
def start(ctx):
  """Starts an existing pde container image"""
  imageYamlFile = open("image.yaml", 'r')
  image = yaml.safe_load(imageYamlFile)

  pdeYamlFile = open("pde.yaml", 'r')
  pde = yaml.safe_load(pdeYamlFile)
  pde.update(image)
  print(yaml.dump(pde))
