# Podman Development Environments (pde)

Containerized development using (rootless) [Podman](https://podman.io/) and 
[CEKit](https://cekit.io/).

We are not building contianer images, instead our focus is on doing day to 
day development *inside* a container. This keeps the development 
environment separate from your desktop or server, allowing you to have 
different sets of tools and libraries installed on either. 

We use [CEKit](https://cekit.io/) 
([GitHub](https://github.com/cekit/cekit)) to provide a modular way of 
describing the tools and libraries in your development environment.

We use (rootless) [Podman](https://podman.io/) 
([GitHub](https://github.com/containers/podman)) to allow flexible access 
to your containerized development environment. 

The only two dependencies required to use pde are: 

1. Podman (rootless),
2. CEKit (and hence Python),

on each compile host.

## Usage

PodmanDevelopmentEnvironments (pde) is a "single" Python command line tool 
consisting of the following subcommands:

0. **config:** This subcommnd lists the current configuration as seen by 
   the ``pde`` command. It also provides some additional help 
   documentation on the various configuration parameters which can be 
   specified in the configuration YAML.

1. **create:** This subcommand creates the "common" development area used 
   by a given pde. This area is common to both the host as well as the 
   running pde container. This allows any artifacts used or built inside 
   the pde to be easily accessible from the host. 

   On the host, this "comnon" directory is, by default, 
   ``~/common/pde/<<pdeName>>``, where ``<<pdeName>>`` is the name of the 
   pde as specified as the first argument to the ``pde`` command. 

   Inside the running pde, this "common" directory is ``/common``.

   Since the pde is run as a rootless podman container, "root" inside the 
   container corresponds to the user on the host who started the pde 
   container. This means that access rights to the files *should* "just 
   work". This also means that "root" inside the running pde has no more 
   privileges on the host than the user who started the pde. 

   The ``create`` subcommand also uses 
   [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)
   to expand the configuration files in the current working directory 
   before copying these configuration files to the "common" area where 
   they are used by all of the other subcommands. Using Jinja2 to expand 
   these configuration files, allows you to keep parameters which are 
   common to the various configuration files in one place. 

2. **destroy:** This subcommand destroys the "common" development area 
   created by the ``create`` subcommand. 

3. **build:** This subcommand uses ``cekit`` to build the podman image 
   used by the pde.

   We use a cekit YAML description to specify what tools and libraries 
   should be included in the running pde. Since we are using cekit we can 
   make use of cekit's modules to allow the overall description of a given 
   pde to (re)use descriptions of composable sub-parts. 

4. **remove:** This subcommand removes any existing podman image 
   associcated with a given pde. 

5. **start:** This subcommand starts a pde using (rootless) podman.

6. **stop:** This subcommand stops a running pde.

7. **enter:** This subcommand opens a shell inside a running pde. You may 
   use this command multiple times to have a number of concurrent shells 
   running inside the pde at the same time. 

   If the host is running Xwindows, then the pde should have access to the 
   running display from inside the container. 

   If the host user has any ssh credentials in the ``~/.ssh`` directory, 
   the pde will have read-only access to these credentials as well. This 
   means that, for example, ssh access to GitHub should work. 

## Configuration

While a small number of configuration parameters can be specified on the 
command line, most of the configuration parameters should be specified in 
one or more configuration files. 

Command line configuration will always take precedence over all other 
confiruration. 

The **global configuration** of both the pde and the cekit commands is 
located in the (command line configurable) global config directory. This 
is by default the ``~/.config/pde`` directory. This directory typically 
contains the ``config.yaml`` and (potentially) the ``cekit.ini`` files.

If it exists, the ``cekit.ini`` file is used by the cekit command (via the 
pde ``build`` subcommand) to configure the cekit command. This 
configuration file uses the "ini" format (all other configuration files 
use the YAML format).

The **local configuration** of both the pde and the cekit commands is 
located in the "common" directory create by the pde ``create`` subcommand. 
This **local configuration** is specific to a given pde and takes 
precedence over any global configuraiton. This configuration consists of 
the following [YAML](https://en.wikipedia.org/wiki/YAML) files: 

  - **image.yaml** This configuration file uses the [cekit descriptor 
    format](https://docs.cekit.io/en/latest/descriptor/index.html)
    to specify how to build a given pde image.

  - **pde.yaml** This configuration file is used by pde to describe how to 
    run a given pde. See the
    [examples/gccLua/pde.yaml](examples/gccLua/pde.yaml)
    example for a brief description of the (optional) keys. 

In addition the **pde ``create`` subcommand** uses the following files 
found in the current working directory: 

  - **image.yaml** This file is a
    [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)
    template which is expanded and copied into the "common" area for a 
    given pde. 

  - **pde.yaml** This file is a
    [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)
    template which is expanded and copied into the "common" area for a 
    given pde. 

  - **Readme.md**  This file is a
    [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)
    template which is expanded and copied into the "common" area for a 
    given pde. It can be used to keep an extended description of how to 
    use the pde. 

  - **config.yaml** This file is loaded as additional local configuration 
    for the ``create`` command. In particluar it can be used to provide 
    additional key/values which can be used by the Jinja2 templates above.

In all cases the Jinja2 templates can use any key/values found in the 
current configuration. You can use the pde ``config`` command to list this 
current configuration as seen by the ``pde`` command(s). 

Similarly, in all cases the YAML format we use is spcified by the 
``pyyaml`` python module. Documentation for this module can be found
[here](https://pyyaml.org/wiki/PyYAMLDocumentation).
Documentation on the YAML syntax used by the ``pyyaml`` module can be found in either 
[Chapter 2 of the YAML specification](http://yaml.org/spec/1.1/#id857168)
or in the 
[the YAML cookbook](https://yaml.org/YAML_for_ruby.html).

**Note** that when using Jinja2 expressions inside a YAML formated file, 
you *will* need to ensure the whole YAML value which uses Jinja2 
expressions is wrapped in quotes. 

## Installation

To install PodmanDevelopmentEnvironments (pde) you must install:

1. **Podman** by following the [Podman installation 
   instructions](https://podman.io/getting-started/installation) 

2. **CEKit** by following the [CEKit installation 
   instructions](https://docs.cekit.io/en/latest/handbook/installation/instructions.html) 

   **NOTE** until CEKit version 3.10 is released, users on Debian based 
   distributions will need to install CEKit directly from the [git 
   repository](https://github.com/cekit/cekit) using the commands:

```
     sudo apt install libkrb5-dev
     pip install git+https://github.com/cekit/cekit.git
```

   If you want CEKit installed for all users, you will need to append 
   ``sudo`` at the begining of the command line above. 

3. **PodmanDevelopmentEnvironments (pde)** itself by using the command:

```
     pip install git+https://github.com/stephengaito/podmanDevelopmentEnvironments.git
```

   Again, if you want pde to be installed for all users, you will need to 
   append ``sudo`` at the begining of the command line above.
