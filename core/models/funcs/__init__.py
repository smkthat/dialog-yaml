from .func import (
    FuncRegistry, function_registry, notify_func, func_wrapper, on_click_wrapper,
    FuncModel, FuncField, NotifyModel
)

func_classes = dict(
    func=FuncModel,
    notify=NotifyModel,
)
