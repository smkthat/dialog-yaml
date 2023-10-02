import pytest

from conftest import func_registry_instance, func_test
from core.core import models_classes
from core.exceptions import BaseModelCreationError, SubModelCreationError
from core.models import YAMLModel
from core.models.funcs import FuncModel


class TestYAMLBaseModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.model_parser = YAMLModel
        self.model_parser._set_classes(models_classes)
        self.func_registry_instance = func_registry_instance

    def test_get_func_model(self, func_registry_instance):
        data = {'func': 'func_test'}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == FuncModel
        assert widget_model.func == func_test

    def test_base_model_error(self, func_registry_instance):
        data = {'unknown': 'func_test'}
        with pytest.raises(BaseModelCreationError):
            self.model_parser.from_data(data)

    def test_sub_model_error(self, func_registry_instance):
        data = {'text': {
            'unknown': 'func_test'
        }}
        with pytest.raises(SubModelCreationError):
            self.model_parser.from_data(data)
