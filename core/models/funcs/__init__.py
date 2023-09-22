from .func import (
    FuncRegistry, notify_func, func_wrapper, on_click_wrapper,
    FuncModel, FuncField, NotifyModel
)

func_classes = dict(
    func=FuncModel,
    when=FuncModel,
    filter=FuncModel,
    getter=FuncModel,
    preview_data=FuncModel,
    on_click=FuncModel,
    on_text_click=FuncModel,
    input_func=FuncModel,
    on_changed=FuncModel,
    notify=NotifyModel,
)
