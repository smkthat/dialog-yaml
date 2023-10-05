import pytest

from core import models_classes
from core.models import YAMLModel
from core.models.funcs import FuncRegistry
from core.states import YAMLStatesBuilder


@pytest.fixture(scope='function')
def func_test():
    def func():
        pass

    return func


data_value = ['a', 'b', 'c']


@pytest.fixture(scope='function')
def get_data():
    def func():
        return data_value

    return func


@pytest.fixture(scope='class')
def func_registry_instance():
    func_registry = FuncRegistry()
    func_registry.func.register(func_test)
    func_registry.func.register(get_data)
    return func_registry


@pytest.fixture(scope='class')
def states_holder_instance():
    states_holder_instance = YAMLStatesBuilder()
    states_holder_instance.parse_raw_states_from_list({
        'TestSG:test1',
        'TestSG:test2',
        'TestSG:test3',
        'Test1SG:test1',
        'Test1SG:test2',
    })
    return states_holder_instance


class TestWidgetBase:
    model_parser_class = None
    func_registry_instance = None
    states_holder_instance = None

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance, states_holder_instance):
        self.model_parser_class = YAMLModel
        self.model_parser_class.set_classes(models_classes)
        self.func_registry_instance = func_registry_instance
        self.states_holder_instance = states_holder_instance
