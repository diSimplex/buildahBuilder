# Buidah Builder

Containerized development using [Buildah](https://buildah.io/) and 
[CEKit](https://cekit.io/).

We are not building contianer images, instead our focus is on doing day to 
day development *inside* a container. This keeps the development 
environment separate from your desktop or server, allowing you to have 
different sets of tools and libraries installed on either. 

We use [CEKit](https://cekit.io/) to provide a modular way of describing 
the tools and libraries in your development environment.

We use [Buildah](https://buildah.io/) to allow flexible access to your 
containerized development environment. 

The only three dependencies required to use BuildahBuilder are:

1. Buildah,
2. CEKit (and hence Python),
3. SSH access to one or more compile hosts.
