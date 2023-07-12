import logging
from abc import ABC, abstractmethod


logging.basicConfig(level=logging.INFO)


class Model(ABC):
    # add any common methods here
    __constraints__ = None
    pass


class World(ABC):
    # add any common methods here
    __constraints__ = None

    @abstractmethod
    def add_model():
        pass

    pass

