from typing import Union, Callable, Awaitable

import pytest

from core.exceptions import FunctionRegistrationError, InvalidFunctionType, CategoryNotFoundError
from core.models.funcs.func import Category, FuncRegistry, CategoryName


@pytest.fixture
def get_test_func() -> Union[Callable, Awaitable]:

    def test_func():
        pass

    return test_func


@pytest.fixture
def registry() -> FuncRegistry:
    registry = FuncRegistry()
    return registry


class TestCategory:

    def test_register_function_successfully(self, get_test_func):
        # Given
        category = Category()
        function = get_test_func

        # When
        category.register(function)

        # Then
        assert category.get(function.__name__) == function

    def test_retrieve_function_successfully(self, get_test_func):
        # Given
        category = Category()
        function = get_test_func
        category.register(function)

        # When
        retrieved_function = category.get(function.__name__)

        # Then
        assert retrieved_function == function

    def test_initialize_category_with_default_name(self):
        # Given/When
        category = Category()

        # Then
        assert category._name == 'func'

    def test_initialize_category_with_custom_name(self):
        # Given
        custom_name = 'custom'

        # When
        category = Category(custom_name)

        # Then
        assert category._name == custom_name

    def test_register_function_with_same_name_twice(self, get_test_func):
        # Given
        category = Category()
        function = get_test_func
        category.register(function)

        # When/Then
        with pytest.raises(FunctionRegistrationError):
            category.register(function)

    def test_retrieve_none_if_function_does_not_exist(self):
        # Given
        category = Category()

        # When
        retrieved_function = category.get('nonexistent_function')

        # Then
        assert retrieved_function is None

    def test_register_non_function_object(self):
        # Given
        category = Category()
        non_callable_object = 123

        # When/Then
        with pytest.raises(InvalidFunctionType):
            category.register(non_callable_object)


class TestFuncRegistry:

    def test_func_property(self, registry):
        # Given
        func = registry.func

        # When/Then
        assert isinstance(func, Category)

    def test_notify_property(self, registry):
        # Given
        func = registry.notify

        # When/Then
        assert isinstance(func, Category)

    def test_get_nonexistent_category(self, registry):
        # Given
        
        # When/Then
        with pytest.raises(CategoryNotFoundError):
            registry.get_category('nonexistent_category')

    def test_register_function_in_notify_category(self, registry, get_test_func):
        # Given
        function = get_test_func

        # When
        registry.register(function, CategoryName.notify)

        # Then
        assert registry.get_function(function.__name__, CategoryName.notify.value) == function

    def test_retrieve_function_from_notify_category(self, registry):
        # Given
        function = get_test_func

        # When
        # registry.notify._functions = {}
        registry.register(function, CategoryName.notify)
        retrieved_function = registry.get_function(function.__name__, CategoryName.notify.value)

        # Then
        assert retrieved_function == function

    def test_register_function_in_custom_category(self, registry):
        # Given
        function = get_test_func
        custom_category = 'custom'

        # When/Then
        with pytest.raises(CategoryNotFoundError):
            registry.register(function, custom_category)
