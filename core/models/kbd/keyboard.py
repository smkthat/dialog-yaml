from functools import partial
from typing import Generic, Union, Self, Any, Annotated

from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Url, Button, SwitchTo, Start, Next, Back, Cancel, Group
from pydantic import field_validator, BeforeValidator

from core.models.base import WidgetModel, T
from core.models.funcs import FuncField
from core.models.funcs.func import NotifyField, FuncModel, func_registry
from core.models.texts import TextField
from core.states import YAMLDialogStatesHolder


class ButtonModel(WidgetModel, Generic[T]):
    id: str = None
    text: TextField

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'text': data}
        return cls(**data)


class UrlButtonModel(ButtonModel, Generic[T]):
    uri: TextField

    def get_obj(self) -> Url:
        kwargs = dict(
            text=self.text.get_obj() if self.text else None,
            url=self.uri.get_obj() if self.uri else None,
            when=self.when.func if self.when else None
        )
        return Url(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'uri': data}
        return cls(**data)


class CallbackButtonModel(ButtonModel, Generic[T]):
    on_click: FuncField = None
    pre_on_click: FuncField = None
    after_on_click: FuncField = None
    notify: NotifyField = None

    def get_partial_on_click(self, on_click: FuncModel = None):
        # if self.notify:
        #     if on_click:
        #         on_click = partial(
        #             func_wrapper,
        #             on_click_func=on_click.func,
        #             on_click_data=on_click.data,
        #             pre_func=self.notify.func,
        #             pre_data=self.notify.notify_data,
        #         )
        #     else:
        #         on_click = partial(
        #             func_wrapper,
        #             on_click_func=self.notify.func,
        #             on_click_data=self.notify.notify_data,
        #         )
        #
        # if self.pre_on_click:
        #     if on_click:
        #         if isinstance(on_click, partial):
        #             on_click = partial(
        #                 func_wrapper,
        #                 on_click_func=on_click.func,
        #                 on_click_data=on_click.keywords.get('on_click_data'),
        #                 pre_func=self.pre_on_click.func,
        #                 pre_data=self.pre_on_click.data,
        #             )
        #         else:
        #             on_click = partial(
        #                 func_wrapper,
        #                 on_click_func=on_click.func,
        #                 on_click_data=on_click.data,
        #                 pre_func=self.pre_on_click.func,
        #                 pre_data=self.pre_on_click.data,
        #             )
        #     else:
        #         on_click = partial(
        #             func_wrapper,
        #             on_click_func=self.pre_on_click.func,
        #             on_click_data=self.pre_on_click.data,
        #         )
        #
        # if self.after_on_click:
        #     if on_click:
        #         if isinstance(on_click, partial):
        #             on_click = partial(
        #                 func_wrapper,
        #                 on_click_func=on_click.func,
        #                 on_click_data=on_click.keywords.get('on_click_data'),
        #                 after_func=self.after_on_click.func,
        #                 after_data=self.after_on_click.data,
        #             )
        #         else:
        #             on_click = partial(
        #                 func_wrapper,
        #                 on_click_func=on_click.func,
        #                 on_click_data=on_click.data,
        #                 after_func=self.after_on_click.func,
        #                 after_data=self.after_on_click.data,
        #             )
        #     else:
        #         on_click = partial(
        #             func_wrapper,
        #             on_click_func=self.after_on_click.func,
        #             on_click_data=self.after_on_click.data,
        #         )
        #
        # return on_click

        partial_data = {
            'on_click_func': on_click.func if on_click else None,
            'on_click_data': on_click.data if on_click else {},
            'pre_click_func': self.pre_on_click.func if self.pre_on_click else None,
            'pre_click_data': self.pre_on_click.data if self.pre_on_click else {},
            'after_click_func': self.after_on_click.func if self.after_on_click else None,
            'after_click_data': self.after_on_click.data if self.after_on_click else {},
            'notify_func': self.notify.func if self.notify else None,
            'notify_data': self.notify.notify_data if self.notify else {},
        }

        def wrap_functions(*args, **kwargs):
            if partial_data['notify_func']:
                partial_data['notify_func'](*args, partial_data['notify_data'])

            if partial_data['pre_click_func']:
                partial_data['pre_click_func'](*args, partial_data['pre_click_data'])

            if partial_data['on_click_func']:
                partial_data['on_click_func'](*args, partial_data['on_click_data'])

            if partial_data['after_click_func']:
                partial_data['after_click_func'](*args, partial_data['after_click_data'])

        on_click = partial(wrap_functions, **partial_data)
        return on_click

    def get_obj(self) -> Button:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = dict(
            text=self.text.get_obj() if self.text else None,
            id=self.id,
            on_click=partial_on_click,
            when=self.when.func if self.when else None
        )
        return Button(**kwargs)


class SwitchToModel(CallbackButtonModel, Generic[T]):
    id: str
    state: str

    def get_obj(self) -> SwitchTo:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = dict(
            id=self.id,
            text=self.text.get_obj() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            state=YAMLDialogStatesHolder().get(self.state)
        )
        return SwitchTo(**kwargs)

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)

    # @field_validator('state')
    # def validate_state(cls, value):
    #     if not value:
    #         return None
    #     if value not in YAMLDialogStatesHolder():
    #         raise ValueError(f'State "{value}" is declared but not provided.')
    #     return value


class StartModel(CallbackButtonModel, Generic[T]):
    id: str
    data: Union[str, int, float, dict[str, Any], list[Any]] = None
    mode: StartMode = StartMode.NORMAL
    state: str

    def get_obj(self) -> Start:
        on_click = self.on_click.func if self.on_click else None
        partial_on_click = self.get_partial_on_click(on_click)
        kwargs = dict(
            id=self.id,
            text=self.text.get_obj() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            state=YAMLDialogStatesHolder().get(self.state),
            data=self.data,
            mode=self.mode
        )
        return Start(**kwargs)

    class Config:
        arbitrary_types_allowed = True

    @field_validator("mode", mode='before')
    def validate_mode(cls, value):
        if isinstance(value, StartMode):
            return value
        elif isinstance(value, str):
            return StartMode[value.upper()]
        else:
            return None

    # @field_validator('state')
    # def validate_state(cls, value):
    #     if not value:
    #         return None
    #     if value not in YAMLDialogStatesHolder():
    #         raise ValueError(f'State "{value}" is declared but not provided.')
    #     return value

    # @classmethod
    # def to_model(cls, data: dict):
    #     return cls(**data)


class NextModel(CallbackButtonModel, Generic[T]):
    text: TextField = None

    def get_obj(self) -> Next:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = dict(
            id=self.id,
            text=self.text.get_obj() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
        )
        return Next(**kwargs)


class BackModel(CallbackButtonModel, Generic[T]):
    text: TextField = None

    def get_obj(self) -> Back:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = dict(
            id=self.id,
            text=self.text.get_obj() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
        )
        return Back(**kwargs)


class CancelModel(CallbackButtonModel):
    text: TextField = None
    result: Any = None

    def get_obj(self) -> Cancel:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = dict(
            id=self.id,
            text=self.text.get_obj() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            result=self.result
        )
        return Cancel(**kwargs)


class GroupKeyboardModel(WidgetModel, Generic[T]):
    id: str = None
    width: int = None
    buttons: list[T]

    def get_obj(self) -> Group:
        kwargs = dict(
            id=self.id,
            width=self.width,
            when=self.when.func if self.when else None
        )
        return Group(
            *[button.get_obj() for button in self.buttons],
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if buttons := data.get('buttons'):
            if isinstance(buttons, str):
                buttons_getter_func = func_registry.func.get(buttons)
                buttons = buttons_getter_func()
            if isinstance(buttons, list):
                data['buttons'] = [cls.from_data(button_data) for button_data in buttons]
        return cls(**data)


GroupKeyboardField = Annotated[GroupKeyboardModel, BeforeValidator(GroupKeyboardModel.to_model)]


class ColumnKeyboardModel(GroupKeyboardModel):
    width: int = 1


class RowKeyboardModel(GroupKeyboardModel):
    width: int = 9999
