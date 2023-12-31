import importlib
import copy
import sys
import logging

import sdformat13 as sdflib

import Factory.Interfaces
import Factory.Exceptions


# ---- Helper functions ----
def create_model_class(input_file: str):

    root = sdflib.Root()
    try:
        # open the file and read into a string and load into root
        sdf_string = ''
        with open(input_file, 'r') as f:
            sdf_string = f.read()
        root.load_sdf_string(sdf_string)
        logging.info("Found new SDF model: " + root.model().name())

    except sdflib.SDFErrorsException as e:
        print(e, file=sys.stderr)
    root = sdflib.Root()

    # create a class from the model
    # maybe use the types package to create a class dynamically?
    class SomeModelClass(Factory.Interfaces.Model):

        def __init__(self):
            self.__root__ = sdflib.Root()
            self.__root__.load_sdf_string(sdf_string)
            self.sdf_model = self.__root__.model()

        def __repr__(self):
            return f'Model({self.sdf_model!r})'

        def print_name(self):
            print(self.sdf_model.name())

        def set_name(self, new_name: str):
            if self.__constraints__ is not None:
                # check if the new name is valid
                if new_name in self.__constraints__["names"]:
                    self.sdf_model.set_name(new_name)
                else:
                    raise Factory.Exceptions.ModelException(
                            SomeModelClass.__name__, "names",
                            self.__constraints__["names"])
        # def set_pose(self, new_pose: list):
        #    if self.__constraints__ is not None:
        #        # check if the new pose is valid
        #        if new_pose in self.__constraints__["pose"]:  # use pySematicPose.raw_pose or something

    # get file name without extension by grepping between the last '/' and '.'
    # if the file is in the current directory, the last '/' is not present
    model_class_name = input_file.split('/')[-1].split('.')[0]
    # Capitalize the first letter
    model_class_name = model_class_name[0].upper() + model_class_name[1:]
    SomeModelClass.__name__ = model_class_name
    logging.info("created class: " + model_class_name)
    return SomeModelClass


def create_world_class(input_file: str):
    root = sdflib.Root()
    try:
        # open the file and read into a string and load into root
        sdf_string = ''
        with open(input_file, 'r') as f:
            sdf_string = f.read()
        root.load_sdf_string(sdf_string)
        logging.info("Found new world SDF model: " +
                     str(root.world_by_index(0).name()))
    except sdflib.SDFErrorsException as e:
        print(e, file=sys.stderr)

    class SomeWorldClass(Factory.Interfaces.World):
        def __init__(self):
            self.__root__ = sdflib.Root()
            self.__root__.load_sdf_string(sdf_string)
            self.sdf_world = self.__root__.world_by_index(0)

        def __repr__(self):
            return f'World({self.sdf_world!r})'

        def print_name(self):
            print(self.sdf_world.name())

        def change_name(self, new_name: str):
            self.sdf_world.set_name(new_name)

        def add_model(self, model: Factory.Interfaces.Model):
            self.sdf_world.add_model(model.sdf_model)

    # get file name without extension by grepping between the last '/' and '.'
    # if the file is in the current directory, the last '/' is not present
    world_class_name = input_file.split('/')[-1].split('.')[0]
    world_class_name = world_class_name[0].upper() + world_class_name[1:]

    SomeWorldClass.__name__ = world_class_name
    return SomeWorldClass


def new_module(mod_name):

    spec = importlib.machinery.ModuleSpec(mod_name, None)
    return importlib.util.module_from_spec(spec)


def create_module(mod_name: str, object_list: list, constraints: dict = {}):

    mod = new_module(mod_name)
    for obj in object_list:
        if obj.__name__ in constraints.keys():
            # create a class with the constraints
            # add the class to the module
            logging.info("adding constraints to <" + str(obj.__name__) + ">")
            obj.__constraints__ = constraints[obj.__name__]
        setattr(mod, obj.__name__, obj)

    sys.modules[mod_name] = mod
    return mod
