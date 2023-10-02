import pytest

from conftest import func_test, func_registry_instance
from core.exceptions import (
    MissingFunctionName,
    MissingFunctionCategoryName,
    InvalidFunctionType,
    FunctionRegistrationError
)
from core.models.funcs import (
    FuncModel,
    NotifyModel,
    notify_func
)


class TestFuncRegistry:
    def test_register_function(self, func_registry_instance):
        func_registry_instance.func.register(func_test)
        assert 'func_test' in func_registry_instance.func
        assert func_registry_instance.func.get('func_test') == func_test

    def test_register_function_from_category(self, func_registry_instance):
        func_registry_instance.func.register(func_test)
        assert 'func_test' in func_registry_instance.func
        assert func_registry_instance.func.get('func_test') == func_test

    def test_get_function(self, func_registry_instance):
        func_registry_instance.func.register(func_test)
        retrieved_function = func_registry_instance.get('func', 'func_test')
        assert retrieved_function == func_test

    def test_get_category(self, func_registry_instance):
        func_registry_instance.func.register(func_test)
        retrieved_category = func_registry_instance.get_category('func')
        assert retrieved_category == func_registry_instance.func

    def test_invalid_function_type(self, func_registry_instance):
        with pytest.raises(InvalidFunctionType):
            func_registry_instance.func.register('this_is_a_string_not_a_function')

    def test_missing_function_name(self):
        data = {'name': ''}
        with pytest.raises(MissingFunctionName):
            FuncModel(**data)

    def test_function_registration_error(self):
        data = {'category_name': 'func', 'name': 'non_existent_function'}
        with pytest.raises(FunctionRegistrationError):
            FuncModel(**data)

    def test_missing_category(self):
        data = {'category_name': 'non_existing_category_name', 'name': 'func_test'}
        with pytest.raises(MissingFunctionCategoryName):
            FuncModel(**data)


class TestFuncModelBase:
    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.func_registry_instance = func_registry_instance
        self.model_class = FuncModel
        self.func_registry_instance.func.register(func_test)

    def test_valid_model(self):
        data = {
            'category_name': self.model_class.model_fields['category_name'].default,
            'name': 'func_test'
        }
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'func_test'
        assert model_instance.func is func_test

    def test_to_model(self):
        data = 'func_test'
        model_instance = self.model_class.to_model(data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'func_test'
        assert model_instance.func is func_test


class TestNotifyModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.func_registry_instance = func_registry_instance
        self.model_class = NotifyModel
        self.func_registry_instance.notify.register(function=func_test)

    def test_valid_notify_model_with_short_data(self):
        data = {'text': 'Test NotifyModel initialization'}
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'notify_func'
        assert model_instance.func is notify_func

    def test_valid_notify_model_with_full_data(self):
        data = {
            'category_name': self.model_class.model_fields['category_name'].default,
            'name': 'func_test',
            'text': 'Test NotifyModel initialization',
            'show_alert': False,
            'delay': None
        }
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'func_test'
        assert model_instance.func is func_test

    def test_notify_to_model(self):
        data = 'Test NotifyModel initialization'
        model_instance = self.model_class.to_model(data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'notify_func'
        assert model_instance.text == data
        assert model_instance.func is notify_func

    def test_notify_get_data(self):
        data = 'Test NotifyModel get data'
        model_instance = self.model_class.to_model(data)
        assert model_instance.notify_data == {
            'text': data,
            'show_alert': False,
            'delay': None
        }
