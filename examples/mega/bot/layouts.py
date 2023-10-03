from core.models.funcs import FuncRegistry


def get_fruit_item(x):
    return x


def register_layouts(dialog_yaml: FuncRegistry):
    dialog_yaml.func.register(get_fruit_item)
