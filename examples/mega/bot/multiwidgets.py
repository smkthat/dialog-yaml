from core import FuncRegistry


def item_id_getter(x, *args, **kwargs):
    return x


def register_multiwidgets(dialog_yaml: FuncRegistry):
    dialog_yaml.func.register(item_id_getter)
