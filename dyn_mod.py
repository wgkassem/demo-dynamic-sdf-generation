# The following script generate a module dynamically `my_module`
# and adds a model a class `Pnedulum` from the sdf file "pendulum.sdf" to it.

import sys
import yaml
import logging

import sdformat13 as sdflib

import Factory


logging.basicConfig(level=logging.INFO)


def export_world_to_sdf(world, output_file: str):  # friend function
    # export the world to sdf file using the root
    root = sdflib.Root()
    root.add_world(world.sdf_world)
    sdf_string = root.to_string()
    with open(output_file, 'w') as f:
        f.write(sdf_string)


def main():
    # create a module dynamically
    mod_name = 'my_module'
    object_list = [Factory.create_model_class('pendulum.sdf'),
                   Factory.create_model_class("pendulum1.sdf"),
                   Factory.create_world_class("pendulum_world.sdf")]
    # read constraints.yml file into a dictionary
    constraints = {}
    with open('constraints.yml', 'r') as f:
        constraints = yaml.safe_load(f)
        logging.info("constraints found: "
                     + str(constraints))

    mod = Factory.create_module(mod_name, object_list, constraints)
    # export the module to the global namespace
    logging.debug("my_module now contains: " + str(dir(mod)))
    # add to sys.modules under package name "my_generation"
    # remove the module if it already exists
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    logging.info("Creating objects")
    world = mod.Pendulum_world()
    model1 = mod.Pendulum()
    model2 = mod.Pendulum1()

    logging.info("Trying illegal rename operation")
    try:
        model2.set_name("pendulum")
    except Factory.ModelException as e:  # maybe add the exception class to my_module
        logging.info("   ... Succefully captured constraint violation")
        logging.error(e)

    world.add_model(model1)
    world.add_model(model2)
    model1.set_name("pendulum2")

    export_world_to_sdf(world, "pendulum_world_generated.sdf")

    sys.modules[mod_name] = mod


def main2():
    # import the exported module and create an object from it
    import my_module
    model = my_module.Pendulum()
    logging.info("Created objects from the module in a different scope, sdf model name: "
                 + model.sdf_model.name())


if __name__ == '__main__':
    main()
    main2()
