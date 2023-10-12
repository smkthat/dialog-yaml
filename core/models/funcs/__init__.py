from .func import (
    FuncsRegistry,
    function_registry,
    notify_func,
    FuncModel,
    FuncField,
    NotifyModel,
    NotifyField,
)

func_classes = dict(
    func=FuncModel,
    notify=NotifyModel,
)
