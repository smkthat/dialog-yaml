import asyncio
from types import FunctionType
from typing import (TypeVar, Generic, Optional, Dict, Union, Any, Callable, Awaitable)

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from pydantic import constr, model_validator

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

    # def register(self, category_name: str, func):
    #     category = self.get_category(category_name)
    #     category.register(func)


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
    def check_init(self):
        category_name = self.category_name
        func_name = self.name
        f = func_registry.get(category_name, func_name)
        return self

    @classmethod
    def to_model(cls, data: Union[str, Dict]) -> T:
        if isinstance(data, str):
            data = {
                'category_name': cls.model_fields['category_name'].default,
                'name': data
            }
        return cls(**data)


class NotifyModel(FuncModel, Generic[T]):
    category_name: str = 'notify'
    name: str = 'notify_func'
    text: constr(strip_whitespace=True, min_length=1, max_length=200)
    show_alert: Optional[bool] = False
    delay: Optional[int] = None

    @property
    def notify_data(self) -> Dict:
        return dict(
            text=self.text,
            show_alert=self.show_alert,
            delay=self.delay
        )

    @classmethod
    def to_model(cls, data: Union[str, Dict]) -> T:
        if isinstance(data, str):
            data = {
                'text': data,
                'name': cls.model_fields['name'].default,
                'category_name': cls.model_fields['category_name'].default,
                'delay': cls.model_fields['delay'].default,
                'show_alert': cls.model_fields['show_alert'].default
            }
        return cls(**data)
