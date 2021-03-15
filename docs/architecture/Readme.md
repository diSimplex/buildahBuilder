# Buildah Builder Architecture

In reality this project is a very simple wrapper around both
[Buildah](https://buildah.io/) 
([GitHub](https://github.com/containers/buildah)) and 
[CEKit](https://cekit.io/) 
([GitHub](https://github.com/cekit/cekit)).

As such this project really only gives an example of using CEKit and 
Buildah together to containerize a development infrastructure. 

We use CEKit to pre-build the development container with all of the 
required tools and libraries. 

We use Buildah to allow a developer to gain direct *"shell"* access to the 
code being developed. 



## Questions

1. Can we have network access to processes running in a development 
   conainer? 

2. Can processes running in a development container interact with X11 
   displays? 


## Notes

CEKit builds an image (but does not create any corresponding (running) 
containers). The image created will be tagged with the value of the name 
field in the CEKit description YAML file. 

