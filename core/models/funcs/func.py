import asyncio
from types import FunctionType
from typing import (TypeVar, Generic, Optional, Dict, Union, Any, Callable, Awaitable, Self, Annotated)

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from pydantic import constr, model_validator, BeforeValidator

from core.exceptions import (
    FunctionRegistrationError,
    InvalidFunctionType,
    MissingFunctionName,
    MissingFunctionCategoryName
)
from core.models import YAMLModel

T = TypeVar('T', bound='FuncModel')


class FuncRegistry:
    class Category(Dict):
        def register(self, function: Union[Callable, Awaitable]):
            if not isinstance(function, FunctionType):
                raise InvalidFunctionType(str(function))
            self[function.__name__] = function

        def get(self, function_name: str):
            return super().get(function_name)

    func = Category()
    notify = Category()

    def get_category(self, name: str) -> Category:
        try:
            return getattr(self, name)
        except AttributeError:
            raise MissingFunctionCategoryName(name)

    def get(self, category_name: str, function_name: str) -> FunctionType:
        if not function_name:
            raise MissingFunctionName(category_name)
        category = self.get_category(category_name)
        function = category.get(function_name)
        if not function:
            raise FunctionRegistrationError(category_name, function_name)
        return function


async def notify_func(callback: CallbackQuery, button: Keyboard, manager: DialogManager, data: Dict = None):
    if data:
        if delay := data.get('delay'):
            await asyncio.sleep(delay=delay)
    await callback.answer(
        **data
    )


func_registry = FuncRegistry()
func_registry.notify.register(function=notify_func)


class FuncModel(YAMLModel, Generic[T]):
    category_name: str = 'func'
    name: str
    data: Optional[Dict[Any, Any]] = {}

    class Config:
        arbitrary_types_allowed = True

    @property
    def func(self):
        f = func_registry.get(self.category_name, self.name)
        return f

    @model_validator(mode='after')
    def check_func(self) -> Self:
        category_name = self.category_name
        func_name = self.name
        f = func_registry.get(category_name, func_name)
        return self

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> T:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'name': data}
        return cls(**data)


FuncField = Annotated[FuncModel, BeforeValidator(FuncModel.to_model)]


class NotifyModel(FuncModel, Generic[T]):
    category_name: str = 'notify'
    name: str = 'notify_func'
    text: constr(strip_whitespace=True, min_length=1, max_length=200)
    show_alert: bool = False
    delay: Union[int, None] = None

    @property
    def notify_data(self) -> Dict:
        return dict(
            text=self.text,
            show_alert=self.show_alert,
            delay=self.delay
        )

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            if val := data.pop('val'):
                data['text'] = val
        if isinstance(data, str):
            data = {
                'text': data,
                'name': cls.model_fields['name'].default,
                'category_name': cls.model_fields['category_name'].default,
                'delay': cls.model_fields['delay'].default,
                'show_alert': cls.model_fields['show_alert'].default
            }
        return cls(**data)


NotifyField = Annotated[NotifyModel, BeforeValidator(NotifyModel.to_model)]


async def func_wrapper(
    *args,
    **kwargs
):
    if pre_func := kwargs.get('pre_func'):
        pre_data = kwargs.get('pre_data')
        await pre_func(*args, pre_data)

    if on_click_func := kwargs.get('on_click_func'):
        on_click_data = kwargs.get('on_click_data')
        await on_click_func(*args, on_click_data)

    pass


async def on_click_wrapper(
    callback: CallbackQuery,
    button: Keyboard,
    manager: DialogManager,
    on_click_func: Union[Callable, Awaitable],
    pre_on_click_func: Union[Callable, Awaitable],
    pre_on_click_data: Optional[Dict],
    after_on_click_func: Union[Callable, Awaitable],
    after_on_click_data: Optional[Dict],
):
    if pre_on_click_func:
        await pre_on_click_func(callback, pre_on_click_data)

    await on_click_func(callback, button, manager)

    if after_on_click_func:
        await after_on_click_func(callback, after_on_click_data)
