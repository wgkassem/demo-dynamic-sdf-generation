# Description

Create a project Python module and classes (model, world/site, soil, ...) associated with the project dynamicall.

The model and world classes are created from sdf files by parsing for `<model>`, `<world>`,
The constraints are defined in YAML files (TBC). They should place constraints on setter fucntions within the classes.

The constrains should define the rules for generating sdf from the classes that are created

# How to run

1. [Install sdformat from source or binaries](http://sdformat.org/tutorials?tut=install)
2. `python3 dyn_mod.sdf`

# Features

1. Dynamic modules
1. Dynamic classes
1. Class unary constraint validation from YAML

# Roadmap

## World/Site

- Constrainable attributes:
    - timestep
    - number of static models
    - number of non-static models
    - collision (positioning) i.e. overlapping objects

- Model:
    - TBD

- Binary constraints (conditional constraints between different classes)
