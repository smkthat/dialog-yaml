from .keyboard import (
    ButtonModel,
    UrlButtonModel,
    CallbackButtonModel,
    SwitchToModel,
    StartModel,
    NextModel,
    BackModel,
    CancelModel,
    GroupKeyboardModel,
    RowKeyboardModel,
    ColumnKeyboardModel,
    ScrollingGroupKeyboardModel,

    GroupKeyboardField
)

keyboard_classes = dict(
    button=ButtonModel,
    url=UrlButtonModel,
    callback=CallbackButtonModel,
    switch_to=SwitchToModel,
    start=StartModel,
    next=NextModel,
    back=BackModel,
    cancel=CancelModel,
    group=GroupKeyboardModel,
    row=RowKeyboardModel,
    column=ColumnKeyboardModel,
    scrolling_group=ScrollingGroupKeyboardModel,
)
