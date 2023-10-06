from typing import Union, Callable, Awaitable

import pytest

from core import models_classes
from core.models import YAMLModel
from core.models.funcs import FuncRegistry
from core.states import YAMLStatesBuilder


@pytest.fixture
def get_test_func() -> Union[Callable, Awaitable]:

    def test_func():
        pass

    return test_func


@pytest.fixture
def get_test_notify() -> Union[Callable, Awaitable]:

    def notify_func():
        pass

    return notify_func


data_value = ['a', 'b', 'c']


@pytest.fixture
def get_test_getter():
    def test_getter():
        return data_value

    return test_getter


@pytest.fixture
def func_registry(get_test_func, get_test_notify, get_test_getter) -> FuncRegistry:
    registry = FuncRegistry()
    registry.clear_categories()
    registry.func.register(get_test_func)
    registry.func.register(get_test_getter)
    registry.notify.register(get_test_notify)
    return registry


@pytest.fixture
def states_builder():
    states_builder = YAMLStatesBuilder()
    states = states_builder.parse_raw_states_from_list({
        'group1:state1',
        'group1:state2',
        'group1:state3',
        'group2:state1',
        'group2:state2',
    })
    states_builder._states_groups_map_.update(states)
    return states_builder


class TestWidgetBase:
    yaml_model = None
    func_registry = None
    states_builder = None

    @pytest.fixture(autouse=True)
    def setup(self, func_registry, states_builder):
        self.yaml_model = YAMLModel
        self.yaml_model.set_classes(models_classes)
        self.func_registry = func_registry
        self.states_builder = states_builder
