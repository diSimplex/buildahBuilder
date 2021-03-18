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

The only three dependencies required to use PodmanBuilder are: 

1. Podman (rootless),
2. CEKit (and hence Python),
3. POSIX shell

on each compile host.
