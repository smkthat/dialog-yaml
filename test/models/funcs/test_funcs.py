from typing import Union, Callable, Awaitable

import pytest

from core.exceptions import (
    FunctionNotFoundError,
    DialogYamlException,
    CategoryNotFoundError,
)
from core.models.funcs.func import CategoryName, FuncModel, FuncsRegistry


@pytest.fixture
def get_test_func() -> Union[Callable, Awaitable]:
    def test_func():
        pass

    return test_func


@pytest.fixture
def registry(get_test_func) -> FuncsRegistry:
    registry = FuncsRegistry()
    registry.func.register(get_test_func)
    return registry


class TestFuncModel:
    def test_create_instance_with_valid_name_and_category_name(self, registry):
        # Given
        name = "test_func"
        category_name = CategoryName.func.value

        # When
        func_model = FuncModel(name=name, category_name=category_name)

        # Then
        assert func_model.name == name
        assert func_model.category_name == category_name

    def test_create_instance_with_valid_name_and_default_category_name(self):
        # Given
        name = "test_func"

        # When
        func_model = FuncModel(name=name)

        # Then
        assert func_model.name == name
        assert func_model.category_name == CategoryName.func.value

    def test_call_to_model_method_with_valid_data(self):
        # Given
        data = {"name": "test_func", "category_name": CategoryName.func.value}

        # When
        func_model = FuncModel.to_model(data)

        # Then
        assert isinstance(func_model, FuncModel)
        assert func_model.name == data["name"]
        assert func_model.category_name == data["category_name"]

    def test_call_func_property_with_valid_function_name_and_category_name(self):
        # Given
        name = "test_func"
        category_name = CategoryName.func.value
        func_model = FuncModel(name=name, category_name=category_name)

        # When
        result = func_model.func

        # Then
        assert result is not None

    def test_create_instance_with_invalid_category_name(self):
        # Given
        name = "test_func"
        category_name = "invalid_category"

        # When/Then
        with pytest.raises(CategoryNotFoundError):
            FuncModel(name=name, category_name=category_name)

    #  Create instance with invalid name
    def test_create_instance_with_invalid_name(self):
        # Given
        name = ""
        category_name = CategoryName.func.value

        # When/Then
        with pytest.raises(FunctionNotFoundError):
            FuncModel(name=name, category_name=category_name)

    def test_call_to_model_method_with_invalid_data(self):
        # Given
        data = {"name": "", "category_name": CategoryName.func.value}

        # When/Then
        with pytest.raises(DialogYamlException):
            FuncModel.to_model(data)

    def test_call_check_func_method_with_invalid_function(self):
        # Given
        name = "invalid_function"
        category_name = CategoryName.func.value

        # When/Then
        with pytest.raises(FunctionNotFoundError):
            FuncModel(name=name, category_name=category_name)

    def test_to_model_with_string_data(self):
        # Given
        data = "test_func"

        # When
        model = FuncModel.to_model(data)

        # Then
        assert isinstance(model, FuncModel)
        assert model.name == "test_func"
        assert model.category_name == CategoryName.func.value
        assert model.data == {}

    def test_to_model_with_dict_data(self):
        # Given
        data = {"name": "test_func", "data": {"param1": "value1", "param2": "value2"}}

        # When
        model = FuncModel.to_model(data)

        # Then
        assert isinstance(model, FuncModel)
        assert model.name == "test_func"
        assert model.category_name == CategoryName.func.value
        assert model.func is not None
        assert model.data == {"param1": "value1", "param2": "value2"}
