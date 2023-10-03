class DialogYamlException(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class BaseModelCreationError(DialogYamlException):
    def __init__(self, model_name, data):
        self.model_name = model_name
        message = f'Error while creating YAMLBaseModel for {model_name!r} with data {data}'
        super().__init__(message)


class ModelRegistrationError(DialogYamlException):
    def __init__(self, tag, model_class, message):
        self.tag = tag
        self._class = model_class
        message.format(tag=tag, model_class=model_class)
        super().__init__(message)


class FunctionRegistrationError(DialogYamlException):
    def __init__(self, category_name, function_name):
        self.function_name = function_name
        message = f'Function {function_name!r} not registered in category {category_name!r}'
        super().__init__(message)


class InvalidFunctionType(DialogYamlException):
    def __init__(self, function_name):
        self.function_name = function_name
        message = f'{function_name!r} is not a function'
        super().__init__(message)


class MissingFunctionName(DialogYamlException):
    def __init__(self, category_name):
        self.category_name = category_name
        message = f'The function name is not provided for the {category_name!r} category'
        super().__init__(message)


class MissingFunctionCategoryName(DialogYamlException):
    def __init__(self, category_name):
        self.category_name = category_name
        message = f'Category {category_name!r} not found'
        super().__init__(message)


class InvalidTagName(DialogYamlException):
    def __init__(self, tag: str, message: str):
        self.tag = tag
        message.format(tag=tag)
        super().__init__(message)
