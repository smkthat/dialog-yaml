import pytest

from core.exceptions import (
    MissingFunctionName,
    MissingFunctionCategoryName,
    InvalidFunctionType,
    FunctionRegistrationError
)
from core.models.funcs import (
    FuncModel,
    NotifyModel,
    FuncRegistry,
    notify_func
)


@pytest.fixture(scope='function')
def test_function():
    def func():
        pass
    return func


@pytest.fixture(scope='class')
def func_registry_instance():
    return FuncRegistry()


class TestFuncRegistry:

    def test_register_function(self, func_registry_instance):
        func_registry_instance.func.register(test_function)
        assert 'test_function' in func_registry_instance.func
        assert func_registry_instance.func.get('test_function') == test_function

    def test_register_function_from_category(self, func_registry_instance):
        func_registry_instance.func.register(test_function)
        assert 'test_function' in func_registry_instance.func
        assert func_registry_instance.func.get('test_function') == test_function

    def test_get_function(self, func_registry_instance):
        func_registry_instance.func.register(test_function)
        retrieved_function = func_registry_instance.get('func', 'test_function')
        assert retrieved_function == test_function

    def test_get_category(self, func_registry_instance):
        func_registry_instance.func.register(test_function)
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
        data = {'category_name': 'non_existing_category_name', 'name': 'test_function'}
        with pytest.raises(MissingFunctionCategoryName):
            FuncModel(**data)


@pytest.mark.parametrize("model_class", [FuncModel])
class TestFuncModelBase:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance, model_class):
        self.func_registry_instance = func_registry_instance
        self.model_class = model_class
        self.func_registry_instance.func.register(test_function)

    def test_valid_model(self):
        data = {
            'category_name': self.model_class.model_fields['category_name'].default,
            'name': 'test_function'
        }
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'test_function'
        assert model_instance.func is test_function

    def test_to_model(self):
        data = 'test_function'
        model_instance = self.model_class.to_model(data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'test_function'
        assert model_instance.func is test_function


class TestNotifyModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.func_registry_instance = func_registry_instance
        self.model_class = NotifyModel
        self.func_registry_instance.notify.register(function=test_function)

    def test_valid_notify_model_with_short_data(self):
        data = {'text': 'Test NotifyModel initialization'}
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'notify_func'
        assert model_instance.func is notify_func

    def test_valid_notify_model_with_full_data(self):
        data = {
            'category_name': self.model_class.model_fields['category_name'].default,
            'name': 'test_function',
            'text': 'Test NotifyModel initialization',
            'show_alert': False,
            'delay': None
        }
        model_instance = self.model_class(**data)
        assert model_instance.category_name == self.model_class.model_fields['category_name'].default
        assert model_instance.name == 'test_function'
        assert model_instance.func is test_function

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
