from functools import partial
from typing import Union, Self, Any, Annotated

from aiogram.fsm.state import State
from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Url, Button, SwitchTo, Start, Next, Back, Cancel, Group, ScrollingGroup
from pydantic import field_validator, BeforeValidator

from core.models import YAMLModelFactory
from core.models.base import WidgetModel
from core.models.funcs import FuncField, NotifyField, FuncModel, function_registry
from core.models.widgets.texts import TextField
from core.states import YAMLStatesBuilder
from core.utils import clean_empty


class ButtonModel(WidgetModel):
    id: str = None
    text: TextField

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if not data:
            return cls()
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'text': data}
        return cls(**data)


class UrlButtonModel(ButtonModel):
    uri: TextField

    def to_object(self) -> Url:
        kwargs = clean_empty(dict(
            text=self.text.to_object() if self.text else None,
            url=self.uri.to_object() if self.uri else None,
            when=self.when.func if self.when else None
        ))
        return Url(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'uri': data}
        return cls(**data)


class CallbackButtonModel(ButtonModel):
    on_click: FuncField = None
    pre_on_click: FuncField = None
    after_on_click: FuncField = None
    notify: NotifyField = None

    def get_partial_on_click(self, on_click: FuncModel = None):
        partial_data = clean_empty({
            'on_click_func': on_click.func if on_click else None,
            'on_click_data': on_click.data if on_click else {},
            'pre_click_func': self.pre_on_click.func if self.pre_on_click else None,
            'pre_click_data': self.pre_on_click.data if self.pre_on_click else {},
            'after_click_func': self.after_on_click.func if self.after_on_click else None,
            'after_click_data': self.after_on_click.data if self.after_on_click else {},
            'notify_func': self.notify.func if self.notify else None,
            'notify_data': self.notify.notify_data if self.notify else {},
        })

        def wrap_functions(*args, **kwargs):
            if partial_data['notify_func']:
                partial_data['notify_func'](*args, partial_data['notify_data'])

            if partial_data['pre_click_func']:
                partial_data['pre_click_func'](*args, partial_data['pre_click_data'])

            if partial_data['on_click_func']:
                partial_data['on_click_func'](*args, partial_data['on_click_data'])

            if partial_data['after_click_func']:
                partial_data['after_click_func'](*args, partial_data['after_click_data'])
        if partial_data:
            on_click = partial(wrap_functions, **partial_data)
        return on_click

    def to_object(self) -> Button:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = clean_empty(dict(
            text=self.text.to_object() if self.text else None,
            id=self.id,
            on_click=partial_on_click,
            when=self.when.func if self.when else None
        ))
        return Button(**kwargs)


class SwitchToModel(CallbackButtonModel):
    id: str
    state: State

    def to_object(self) -> SwitchTo:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = clean_empty(dict(
            id=self.id,
            text=self.text.to_object() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            state=self.state
        ))
        return SwitchTo(**kwargs)

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)

    @field_validator('state', mode='before')
    def validate_state(cls, value) -> State:
        state = YAMLStatesBuilder().get_by_name(value)
        if not state:
            raise ValueError(f'State "{value}" is declared but not provided.')
        return state


class StartModel(CallbackButtonModel):
    id: str
    data: Union[str, int, float, dict[str, Any], list[Any]] = None
    mode: StartMode = StartMode.NORMAL
    state: State

    def to_object(self) -> Start:
        on_click = self.on_click.func if self.on_click else None
        partial_on_click = self.get_partial_on_click(on_click)
        kwargs = clean_empty(dict(
            id=self.id,
            text=self.text.to_object() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            state=self.state,
            data=self.data,
            mode=self.mode
        ))
        return Start(**kwargs)

    @field_validator('state', mode='before')
    def validate_state(cls, value) -> State:
        state = YAMLStatesBuilder().get_by_name(value)
        if not state:
            raise ValueError(f'State "{value}" is declared but not provided.')
        return state

    @field_validator('mode', mode='before')
    def validate_mode(cls, value):
        if isinstance(value, StartMode):
            return value
        elif isinstance(value, str):
            return StartMode[value.upper()]
        else:
            return None


class NextModel(CallbackButtonModel):
    text: TextField = None

    def to_object(self) -> Next:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = clean_empty(dict(
            id=self.id,
            text=self.text.to_object() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
        ))
        return Next(**kwargs)


class BackModel(CallbackButtonModel):
    text: TextField = None

    def to_object(self) -> Back:
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = clean_empty(dict(
            id=self.id,
            text=self.text.to_object() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
        ))
        return Back(**kwargs)


class CancelModel(CallbackButtonModel):
    text: TextField = None
    result: Union[FuncField, Any] = None

    def to_object(self) -> Cancel:
        result = self.result
        if isinstance(result, FuncModel):
            result = result.func
        partial_on_click = self.get_partial_on_click(self.on_click)
        kwargs = clean_empty(dict(
            id=self.id,
            text=self.text.to_object() if self.text else None,
            on_click=partial_on_click,
            when=self.when.func if self.when else None,
            result=result
        ))
        return Cancel(**kwargs)


class GroupKeyboardModel(WidgetModel):
    id: str = None
    width: int = None
    buttons: list[WidgetModel]

    def to_object(self) -> Group:
        kwargs = clean_empty(dict(
            id=self.id,
            width=self.width,
            when=self.when.func if self.when else None
        ))
        return Group(
            *[button.to_object() for button in self.buttons],
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            if buttons := data.get('buttons'):
                if isinstance(buttons, str):
                    buttons_getter_func = function_registry.func.get(buttons)
                    buttons = buttons_getter_func()
                if isinstance(buttons, list):
                    data['buttons'] = [YAMLModelFactory.create_model(button_data) for button_data in buttons]
        return cls(**data)


GroupKeyboardField = Annotated[GroupKeyboardModel, BeforeValidator(GroupKeyboardModel.to_model)]


class ColumnKeyboardModel(GroupKeyboardModel):
    width: int = 1


class RowKeyboardModel(GroupKeyboardModel):
    width: int = 9999


class ScrollingGroupKeyboardModel(GroupKeyboardModel):
    id: str
    height: int = 1
    on_page_changed: FuncField = None
    hide_on_single_page: bool = False
    hide_pager: bool = False

    def to_object(self) -> ScrollingGroup:
        kwargs = clean_empty(dict(
            id=self.id,
            height=self.height,
            width=self.width,
            on_page_changed=self.on_page_changed.func if self.on_page_changed else None,
            hide_on_single_page=self.hide_on_single_page,
            hide_pager=self.hide_pager
        ))
        return ScrollingGroup(
            *[button.to_object() for button in self.buttons],
            **kwargs
        )
