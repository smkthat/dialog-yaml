import asyncio
from enum import Enum
from types import FunctionType
from typing import (Optional, Dict, Union, Any, Callable, Awaitable, Self, Annotated, Literal)

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from pydantic import constr, model_validator, BeforeValidator, ConfigDict

from core.exceptions import (
    FunctionRegistrationError,
    InvalidFunctionType,
    MissingFunctionName,
    CategoryNotFoundError, FunctionNotFoundError
)
from core.models import YAMLModel


class CategoryName(Enum):
    FUNC = 'func'
    NOTIFY = 'notify'


class Category(Dict):
    name: str

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def register(self, function: Union[Callable, Awaitable]):
        if not isinstance(function, FunctionType):
            raise InvalidFunctionType(str(function))

        function_name = function.__name__
        if function_name in self:
            raise FunctionRegistrationError(
                self.name, function_name
            )

        self[function_name] = function

    def get(self, function_name: str):
        function = super().get(function_name)

        if function:
            return function

        raise FunctionNotFoundError(self.name, function_name)


class FuncRegistry:
    _categories_: Dict[str, Category] = {
        category_name.value: Category(category_name.value)
        for category_name in CategoryName
    }

    @property
    def func(self):
        return self._categories_[CategoryName.FUNC.value]

    @property
    def notify(self):
        return self._categories_[CategoryName.NOTIFY.value]

    def register(self, function: Union[Callable, Awaitable], category_name: CategoryName = CategoryName.FUNC):
        match category_name:
            case CategoryName.NOTIFY:
                self.get_category(category_name.value).register(function)
            case CategoryName.FUNC:
                self.get_category(category_name.value).register(function)
            case _:
                category = self.get_category(category_name.value)
                if category is not None:
                    category.register(function)

    def get_category(self, name: str = CategoryName.FUNC.value) -> Category:
        category = self._categories_.get(name)

        if category is not None:
            return category

        raise CategoryNotFoundError(name)

    def get_function(self, function_name: str, category_name: str = CategoryName.FUNC.value) -> Union[
        Callable, Awaitable]:
        category = self.get_category(category_name)
        function = category.get(function_name)
        return function


async def notify_func(callback: CallbackQuery, data: Dict = None, *args, **kwargs) -> None:
    if data:
        if delay := data.get('delay'):
            await asyncio.sleep(delay=delay)
    await callback.answer(
        **data
    )


function_registry = FuncRegistry()
function_registry.notify.register(function=notify_func)


class FuncModel(YAMLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    category_name: str = 'func'
    name: str
    data: Optional[Dict[Any, Any]] = {}

    @property
    def func(self):
        f = function_registry.get_function(self.name, self.category_name)
        return f

    @model_validator(mode='after')
    def check_func(self) -> Self:
        category_name = self.category_name
        func_name = self.name
        f = function_registry.get_function(func_name, category_name)
        return self

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'name': data}
        if not data:
            print()
        return cls(**data)


FuncField = Annotated[FuncModel, BeforeValidator(FuncModel.to_model)]


class NotifyModel(FuncModel):
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
