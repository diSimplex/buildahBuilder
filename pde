#!/usr/bin/env python3

# This python3 script starts a pde container

import pdeCmds
import pdeCmds.config
import pdeCmds.create
import pdeCmds.destroy
import pdeCmds.build
import pdeCmds.remove
import pdeCmds.start
import pdeCmds.stop
import pdeCmds.enter

if __name__ == '__main__':
  pdeCmds.cli()
