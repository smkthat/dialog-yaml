from .func import (
    FuncsRegistry, function_registry, notify_func, func_wrapper, on_click_wrapper,
    FuncModel, FuncField, NotifyModel, NotifyField
)

func_classes = dict(
    func=FuncModel,
    notify=NotifyModel,
)
