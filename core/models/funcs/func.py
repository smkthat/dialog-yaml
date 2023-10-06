import asyncio
from enum import Enum
from typing import (Optional, Dict, Union, Any, Callable, Awaitable, Self, Annotated)

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from pydantic import constr, model_validator, BeforeValidator, ConfigDict, BaseModel

from core.decorators import singleton
from core.exceptions import (
    FunctionRegistrationError,
    InvalidFunctionType,
    CategoryNotFoundError, FunctionNotFoundError
)


class CategoryName(Enum):
    """The CategoryName class represents the names of categories for functions.

    :cvar func: The name of the 'func' category.
        This category is used for other functions, such as data getters, setters, filers, conditions, and others.
    :vartype func: CategoryName
    :cvar notify: The name of the 'notify' category.
        This category uses for notification functions
    :vartype notify: CategoryName
    """

    func = 'func'
    notify = 'notify'


class Category:
    """The Category class represents a category of functions and provides methods for registering and retrieving 
    functions within the category.

    :param name: The name of the category, if not provided, the category will be named 'func'.
    :type name: CategoryName

    :ivar _name: The name of the category
    :vartype _name: CategoryName
    """

    _name: str
    _functions: Dict[str, Union[Callable, Awaitable]]

    def __init__(self, name: Union[str, CategoryName] = CategoryName.func):
        self._name = name.value if isinstance(name, CategoryName) else name
        self._functions = {}

    def __str__(self):
        return f"Category(name={self._name}, functions={self._functions})"

    def register(self, function: Union[Callable, Awaitable]):
        """Register a function within the category.

        :param function: The function to register
        :type function: Union[Callable, Awaitable]

        :raises FunctionRegistrationError: If the function is already registered within the category
        :raises InvalidFunctionType: If the function is not a Callable or an Awaitable object
        """

        if not isinstance(function, (Callable, Awaitable)):
            raise InvalidFunctionType(str(function))

        function_name = function.__name__
        if function_name in self._functions:
            raise FunctionRegistrationError(
                self._name, function_name
            )

        self._functions[function_name] = function

    def get(self, function_name: str) -> Union[Callable, Awaitable, None]:
        """Retrieve a function from the category.

        :param function_name: The name of the function to retrieve
        :type function_name: str

        :return: The retrieved function or None if the function is not registered within the category
        :rtype: Union[Callable, Awaitable, None]
        """

        return self._functions.get(function_name)


@singleton
class FuncRegistry:
    """The FuncRegistry class manages the registration and retrieval of functions.

    :ivar _categories_map_: A dictionary of categories
    :vartype _categories_: Dict[str, Category]
    """
    _categories_map_: Dict[str, Category]

    def __init__(self):
        self.clear_categories()

    def clear_categories(self):
        self._categories_map_ = {
            category_name.value: Category(category_name.value)
            for category_name in CategoryName
        }

    @property
    def func(self) -> Category:
        return self._categories_map_[CategoryName.func.value]

    @property
    def notify(self) -> Category:
        return self._categories_map_[CategoryName.notify.value]

    def register(self, function: Union[Callable, Awaitable],
                 category_name: Union[str, CategoryName] = CategoryName.func) -> None:
        """Registers a function in the specified category.

        :param function: The function to be registered.
        :type function: Union[Callable, Awaitable]
        :param category_name: The name of the category. Defaults to `CategoryName.func`.
        :type category_name: Union[str, CategoryName], optional
        """

        if isinstance(category_name, CategoryName):
            category_name = category_name.value

        category = self.get_category(category_name)
        category.register(function)

    def get_category(self, name: str = CategoryName.func.value) -> Category:
        """Retrieves the category with the specified name.

        :param name: The name of the category. Defaults to `func`
        :type name: Union[str, CategoryName]

        :return: The category object.
        :rtype: Category
        """

        category = self._categories_map_.get(name)

        if category is not None:
            return category

        raise CategoryNotFoundError(name)

    def get_function(
            self, function_name: str, category_name: str = CategoryName.func.value
    ) -> Union[Callable, Awaitable]:
        """Retrieves the function with the specified name from the specified category.

        :param category_name: The name of the category. Defaults to `funcs`
        :type category_name: Union[str, CategoryName]
        :param function_name: The name of the function.
        :type function_name: str

        :return: The function object or `None` if not found.
        :rtype: Union[Callable, Awaitable, None]
        """

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


class FuncModel(BaseModel):
    def to_object(self) -> Union[Callable, Awaitable]:
        return self.func

    model_config = ConfigDict(arbitrary_types_allowed=True)

    category_name: str = CategoryName.func.value
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

        if f is None:
            raise FunctionNotFoundError(category_name, func_name)

        return self

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'name': data}
        return cls(**data)


FuncField = Annotated[FuncModel, BeforeValidator(FuncModel.to_model)]


class NotifyModel(FuncModel):
    category_name: str = CategoryName.notify.value
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
    """Asynchronously executes pre_func and on_click_func if provided in kwargs.

    :param args: The arguments.
    :type args: Tuple
    :param kwargs: The keyword arguments.
    :type kwargs: Dict

    :return: None
    :rtype: None
    """

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
    """Executes a series of functions before and after the main on_click function is called.

    :param callback: The callback query.
    :type callback: CallbackQuery
    :param button: The button.
    :type button: Keyboard
    :param manager: The dialog manager.
    :type manager: DialogManager
    :param on_click_func: The on_click function.
    :type on_click_func: Union[Callable, Awaitable]
    :param pre_on_click_func: The pre_on_click function.
    :type pre_on_click_func: Union[Callable, Awaitable]
    :param pre_on_click_data: The pre_on_click data.
    :type pre_on_click_data: Optional[Dict]
    :param after_on_click_func: The after_on_click function.
    :type after_on_click_func: Union[Callable, Awaitable]
    :param after_on_click_data: The after_on_click data.
    :type after_on_click_data: Optional[Dict]

    :return: None
    :rtype: None
    """

    if pre_on_click_func:
        await pre_on_click_func(callback, pre_on_click_data)

    await on_click_func(callback, button, manager)

    if after_on_click_func:
        await after_on_click_func(callback, after_on_click_data)
