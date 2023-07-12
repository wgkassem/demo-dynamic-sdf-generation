import importlib
import copy
import logging
import sys

import sdformat13 as sdflib

logging.basicConfig(level=logging.INFO)


class ModelException(Exception):
    "Exception raised for errors in the creating model objects."

    def __init__(self, model_name: str, constraint_name: str, possible_values: list = None):
        self.model_name = model_name
        self.constraint_name = constraint_name
        self.message = f"Model {model_name} does not satisfy constraint <{constraint_name}>, possible values are {possible_values}"
        super().__init__(self.message)


def create_model_class(input_file: str, class_constraints: dict = None):

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
    class Model:
        __constraints__ = copy.deepcopy(class_constraints)

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
                    raise ModelException(Model.__name__, "names",
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
    Model.__name__ = model_class_name
    logging.info("created class: " + model_class_name)
    return Model


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

    class World:
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

        def add_model(self, model):
            self.sdf_world.add_model(model.sdf_model)

    # get file name without extension by grepping between the last '/' and '.'
    # if the file is in the current directory, the last '/' is not present
    world_class_name = input_file.split('/')[-1].split('.')[0]
    # Capitalize the first letter
    world_class_name = world_class_name[0].upper() + world_class_name[1:]

    World.__name__ = world_class_name
    return World


def new_module(mod_name):

    spec = importlib.machinery.ModuleSpec(mod_name, None)
    return importlib.util.module_from_spec(spec)


def create_module(mod_name, object_list, constraints):

    mod = new_module(mod_name)
    for obj in object_list:
        if obj.__name__ in constraints.keys():
            # create a class with the constraints
            # add the class to the module
            logging.info("adding constraints to <" + str(obj.__name__) + ">")
            obj.__constraints__ = constraints[obj.__name__]
        setattr(mod, obj.__name__, obj)

    return mod

# Add `create_world_class` for addign a world to the module
# Add `create_constraint_class` indicating the type of constraint between two
# classes

