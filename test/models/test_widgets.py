import pytest
from aiogram_dialog.widgets.kbd import Checkbox
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List

from core import models_classes
from core.models import YAMLModel
from core.models.funcs import FuncRegistry, FuncModel
from core.models.selects import CheckboxModel
from core.models.texts import TextModel, FormatModel, MultiTextModel, CaseModel
from core.models.texts.text import ListModel


@pytest.fixture(scope='function')
def test_function():
    def func():
        pass

    return func


@pytest.fixture(scope='function')
def get_data():
    def func():
        return ['a', 'b', 'c']

    return func


@pytest.fixture(scope='class')
def func_registry_instance():
    return FuncRegistry()


class TestWidgetModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.model_parser = YAMLModel
        self.model_parser.set_classes(models_classes)
        self.func_registry_instance = func_registry_instance
        self.func_registry_instance.func.register(test_function)
        self.func_registry_instance.func.register(get_data)

    def test_text_model_str(self):
        val = 'text widget text'
        data = {'text': val}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == TextModel
        assert widget_model.val == val
        assert widget_model.when is None

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Const)

    def test_text_model_dict(self):
        val = 'text widget text'
        data = {'text': {
            'val': val,
            'when': 'test_function'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == TextModel
        assert widget_model.val == val
        assert isinstance(widget_model.when, FuncModel)
        assert widget_model.when.func == test_function

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Const)

    def test_format_model_dict(self):
        val = 'text widget {name}'
        data = {'format': {
            'val': val,
            'when': 'test_function'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == FormatModel
        assert widget_model.val == val
        assert isinstance(widget_model.when, FuncModel)
        assert widget_model.when.func == test_function

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Format)

    def test_multi_model(self):
        val = 'text widget {name}'
        data = {'multi': {
            'texts': [
                {'format': val},
                {'text': {
                    'val': val,
                    'when': 'test_function'
                }}
            ]

        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == MultiTextModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Multi)

    def test_case_model(self):
        data = {'case': {
            'texts': {
                True: "Option: enabled",
                False: "Option: disabled"
            },
            'selector': 'selector_key'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == CaseModel
        assert widget_model.selector == 'selector_key'

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Case)

    def test_case_model2(self):
        data = {'case': {
            'texts': {
                True: "Option: enabled",
                False: "Option: disabled"
            },
            'selector': {'func': 'test_function'}
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == CaseModel
        assert isinstance(widget_model.selector, FuncModel)
        assert widget_model.selector.func == test_function

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Case)

    def test_list_model(self):
        data = {'list': {
            'field': "+ {item.name} - {item.id}",
            'items': 'get_data',
            'when': 'test_function'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == ListModel
        assert isinstance(widget_model.items, FuncModel)
        assert widget_model.items.func == get_data

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, List)

    def test_list_model2(self):
        data = {'list': {
            'field': "+ {item.name} - {item.id}",
            'items': ['a', 'b', 'c', 'd'],
            'when': 'test_function'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == ListModel
        assert widget_model.items == ['a', 'b', 'c', 'd']

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, List)

    def test_checkbox_model(self):
        data = {'checkbox': {
            'checked': "✓ Option is enabled",
            'unchecked': "Click to enable the option",
            'default': False,
            'id': 'chk'
        }}
        widget_model = self.model_parser.from_data(data)
        assert widget_model.__class__ == CheckboxModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Checkbox)
