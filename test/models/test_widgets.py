import pytest
from aiogram_dialog.widgets.kbd import (
    Checkbox, Select, Radio, Url, Button, SwitchTo, Start, Next, Back, Cancel, Group
)
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List

from core import models_classes
from core.models import YAMLModel
from core.models.funcs import FuncRegistry, FuncModel
from core.models.kbd import (
    UrlButtonModel, CallbackButtonModel,
    SwitchToModel, StartModel, NextModel, BackModel, CancelModel,
    GroupKeyboardModel, RowKeyboardModel, ColumnKeyboardModel
)
from core.models.selects import CheckboxModel, SelectModel, RadioModel
from core.models.texts import TextModel, FormatModel, MultiTextModel, CaseModel
from core.models.texts.text import ListModel
from core.states import YAMLDialogStatesHolder


@pytest.fixture(scope='function')
def test_function():
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
    func_registry.func.register(test_function)
    func_registry.func.register(get_data)
    return func_registry


@pytest.fixture(scope='class')
def states_holder_instance():
    states_holder_instance = YAMLDialogStatesHolder()
    states_holder_instance.parse_objs([
        'TestSG:test1',
        'TestSG:test2',
        'TestSG:test3',
        'Test1SG:test1',
        'Test1SG:test2',
    ])
    return states_holder_instance


class TestWidgetModel:

    @pytest.fixture(autouse=True)
    def setup(self, func_registry_instance):
        self.model_parser_class = YAMLModel
        self.model_parser_class.set_classes(models_classes)
        self.func_registry_instance = func_registry_instance
        self.states_holder_instance = states_holder_instance


class TestTextModel(TestWidgetModel):
    def test_text_model_str(self):
        val = 'text widget text'
        data = {'text': val}
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == FormatModel
        assert widget_model.val == val
        assert isinstance(widget_model.when, FuncModel)
        assert widget_model.when.func == test_function

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Format)

    def test_format_model_dict2(self):
        val = 'text widget {name}'
        data = {
            'val': val,
            'when': 'test_function'
        }
        widget_model = FormatModel(**data)
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
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
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
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == ListModel
        assert widget_model.items == ['a', 'b', 'c', 'd']

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, List)


class TestSelectModel(TestWidgetModel):
    def test_checkbox_model(self):
        data = {'checkbox': {
            'checked': "✓ Option is enabled",
            'unchecked': "Click to enable the option",
            'default': False,
            'id': 'chk'
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == CheckboxModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Checkbox)

    def test_select_model(self):
        data = {'select': {
            'format': '{item.name} ({item.id})',
            'id': 'sel',
            'items': 'get_data',
            'item_id_getter': 'test_function',
            'on_click': 'test_function'}
        }
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == SelectModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Select)

    def test_radio_model(self):
        data = {'radio': {
            'checked': '🔘 {item.name}',
            'unchecked': '⚪️ {item.name}',
            'id': 'radio',
            'items': 'get_data',
            'item_id_getter': 'test_function'
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == RadioModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Radio)


class TestKeyboardModel(TestWidgetModel):
    def test_url_button(self):
        data = {'url': {
            'text': 'Url button text',
            'uri': 'https://example.com',
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == UrlButtonModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Url)

    def test_callback_button(self):
        on_click_data = {
            'name': 'get_data',
            'data': {
                'key': 'value'
            }
        }
        data = {'callback': {
            'id': 'callback',
            'text': 'Callback with funcs',
            'on_click': on_click_data,
            'pre_on_click': 'test_function',
            'after_on_click': 'test_function',
            'notify': {
                'val': 'This is alert notify with 3 sec delay',
                'show_alert': True,
                'delay': 3
            }
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == CallbackButtonModel
        assert isinstance(widget_model.on_click, FuncModel)
        assert widget_model.on_click.func == get_data
        assert widget_model.on_click.data == on_click_data['data']

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Button)

    def test_switch_to_button(self):
        data = {'switch_to': {
            'id': 'switch',
            'text': 'Switch to',
            'state': 'TestSG:test1'
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == SwitchToModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, SwitchTo)

    def test_start_button(self):
        data = {'start': {
            'id': 'start',
            'text': 'Start',
            'state': 'TestSG:test1'
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == StartModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Start)

    def test_next_button(self):
        data = {'next': 'Next'}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == NextModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Next)

    def test_back_button(self):
        data = {'back': 'Back'}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == BackModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Back)

    def test_cancel_button(self):
        data = {'cancel': 'Cancel'}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == CancelModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Cancel)

    def test_group_keyboard(self):
        data = {'group': {
            'width': 2,
            'buttons': [
                {'start': {
                    'id': 'start',
                    'text': 'Start',
                    'state': 'TestSG:test1'
                }},
                {'next': {}},
                {'back': {}},
                {'cancel': {}},
            ]
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == GroupKeyboardModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Group)

    def test_row_keyboard(self):
        data = {'row': {
            'buttons': [
                {'start': {
                    'id': 'start',
                    'text': 'Start',
                    'state': 'TestSG:test1'
                }},
                {'next': {}},
                {'back': {}},
                {'cancel': {}},
            ]
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == RowKeyboardModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Group)

    def test_column_keyboard(self):
        data = {'column': {
            'buttons': [
                {'start': {
                    'id': 'start',
                    'text': 'Start',
                    'state': 'TestSG:test1'
                }},
                {'next': {}},
                {'back': {}},
                {'cancel': {}},
            ]
        }}
        widget_model = self.model_parser_class.from_data(data)
        assert widget_model.__class__ == ColumnKeyboardModel

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, Group)
