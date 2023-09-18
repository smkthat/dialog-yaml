class DialogYamlException(RuntimeError):
    message: str


class BaseModelCreationError(DialogYamlException):
    def __init__(self, model_name, data):
        self.model_name = model_name
        self.message = f'Error while creating YAMLBaseModel for {model_name!r} with data {data}'


class SubModelCreationError(DialogYamlException):
    def __init__(self, model_name, data):
        self.model_name = model_name
        self.message = f'Error while creating YAMLSubModel for {model_name!r} with data {data}'


class FunctionRegistrationError(DialogYamlException):
    def __init__(self, category_name, function_name):
        self.function_name = function_name
        self.message = f'Function {function_name!r} not registered in category {category_name!r}'


class InvalidFunctionType(DialogYamlException):
    def __init__(self, function_name):
        self.function_name = function_name
        self.message = f'{function_name!r} is not a function'


class MissingFunctionName(DialogYamlException):
    def __init__(self, category_name):
        self.category_name = category_name
        self.message = f'The function name is not provided for the {category_name!r} category'


class MissingFunctionCategoryName(DialogYamlException):
    def __init__(self, category_name):
        self.category_name = category_name
        self.message = f'Category {category_name!r} not found'
