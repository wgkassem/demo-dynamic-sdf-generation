# Description

Create a project Python module and classes (model, world/site, soil, ...) associated with the project dynamicall.

The model and world classes are created from sdf files by parsing for `<model>`, `<world>`,
The constraints are defined in YAML files (TBC). They should place constraints on setter fucntions within the classes.

The constrains should define the rules for generating sdf from the classes that are created


## World/Site

- Constrainable attributes:
    - timestep
    - number of static models
    - number of non-static models
    - collision (positioning) i.e. overlapping objects

- Model:
    - TBD
