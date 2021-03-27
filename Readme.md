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

1. **config:** This subcommnd lists the current configuration as seen by 
   the ``pde`` command. It also provides some additional help 
   documentation on the various configuration parameters which can be 
   specified in the configuration YAML.

   ----
   
2. **create:** This subcommand creates the "common" development area used 
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

3. **destroy:** This subcommand destroys the "common" development area 
   created by the ``create`` subcommand. 

   ----
   
4. **build:** This subcommand uses ``cekit`` to build the podman image 
   used by the pde.

   We use a cekit YAML description to specify what tools and libraries 
   should be included in the running pde. Since we are using cekit we can 
   make use of cekit's modules to allow the overall description of a given 
   pde to (re)use descriptions of composable sub-parts. 

   The build subcommand takes an optional argument ``--override`` which 
   can be used to specify a CEKit overrides file for building the image. 
   If no ``--override`` options is used, but the pde working directory 
   contains a file named ``override-<<machine>>.yaml`` (where 
   ``<machine>>`` is the result of the Python ``platform.machine()`` 
   method), then this file is automatically used as an override file.

5. **images:** This subcommand lists all images associated with the pde.

6. **remove:** This subcommand removes any existing podman image 
   associcated with a given pde. 

   ----
   
7. **start:** This subcommand starts a pde using (rootless) podman.

8. **stop:** This subcommand stops a running pde.

9. **containers:** This subcommand list all containers associated with the 
   pde. 

10. **enter:** This subcommand opens a shell inside a running pde. You may 
    use this command multiple times to have a number of concurrent shells 
    running inside the pde at the same time. 

    If the host is running Xwindows, then the pde should have access to the 
    running display from inside the container. 

    If the host user has any ssh credentials in the ``~/.ssh`` directory, 
    the pde will have read-only access to these credentials as well. This 
    means that, for example, ssh access to GitHub should work. 

11. **run:** This subcommand runs the command provided inside a running 
    pde. 

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

We have added a ``lookup`` Jinja2 filter which takes the name of a table 
in the configuration and returns the looked up value in the table. See the 
[example/gccLua/config.yaml](examples/gccLua/config.yaml) and 
[example/gccLua/pde.yaml](examples/gccLua/pde.yaml) files for an example
of how to use the ``lookup`` filter. 

We have also added the results of the Python ``platform`` library to the 
configuration. Together with the ``lookup`` filter, this allows you to 
provide a flexible naming system for, for example, CEKit artifacts in your 
``image.yaml`` CEKit description. 

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

## Bash, Zsh and Fish completion scripts

The shellCompletionScripts subdirectory provides Bash, Zsh and Fish 
completion scripts. 

For Bash and Zsh these completion scripts can be sourced in the 
respective, ``~/.bashrc``, ``~/zshrc`` startup scripts. 

For Fish this completion script should be placed in the 
``~/.config/fish/completions`` directory. 

See [Click's Shell Completion 
documentation](https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script) 
for details. 

## Installation

To install PodmanDevelopmentEnvironments (pde) you must install:

1. **Podman** by following the [Podman installation 
   instructions](https://podman.io/getting-started/installation) 

2. **CEKit** by following the [CEKit installation 
   instructions](https://docs.cekit.io/en/latest/handbook/installation/instructions.html) 

   **NOTE** Users on Debian based distros will need to have the
   ``libkrb5-dev`` package installed *before* installing CEKit.
   You can do this using the commands:

   ```
     sudo apt install libkrb5-dev
   ```

3. **PodmanDevelopmentEnvironments (pde)** itself by using the command:

   ```
     pip install git+https://github.com/stephengaito/podmanDevelopmentEnvironments.git
   ```

   Again, if you want pde to be installed for all users, you will need to 
   append ``sudo`` at the begining of the command line above.
