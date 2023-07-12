
class ModelException(Exception):
    "Exception raised for errors in the creating model objects."

    def __init__(self, model_name: str, constraint_name: str, possible_values: list = None):
        self.model_name = model_name
        self.constraint_name = constraint_name
        self.message = f"Model {model_name} does not satisfy constraint <{constraint_name}>, possible values are {possible_values}"
        super().__init__(self.message)
