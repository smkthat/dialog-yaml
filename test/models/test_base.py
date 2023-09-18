import pytest

from core.core import models_classes
from core.exceptions import BaseModelCreationError, SubModelCreationError
from core.models import YAMLModel
from core.models.funcs import (
    FuncRegistry, FuncModel,

)


@pytest.fixture(scope='function')
def test_function():
    def func():
        pass
    return func


@pytest.fixture(scope='class')
def func_registry_instance():
    return FuncRegistry()


class TestYAMLBaseModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.model_parser = YAMLModel
        self.model_parser.set_classes(models_classes)
        self.func_registry_instance = func_registry_instance
        self.func_registry_instance.func.register(test_function)

    def test_get_func_model(self, func_registry_instance):
        data = {'func': 'test_function'}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == FuncModel
        assert widget_model.func == test_function

    def test_base_model_error(self, func_registry_instance):
        data = {'unknown': 'test_function'}
        with pytest.raises(BaseModelCreationError):
            self.model_parser.from_data(data)

    def test_sub_model_error(self, func_registry_instance):
        data = {'text': {
            'unknown': 'test_function'
        }}
        with pytest.raises(SubModelCreationError):
            self.model_parser.from_data(data)
