import pytest
from aiogram_dialog.widgets.kbd import Checkbox, Select, Radio, Multiselect

from conftest import TestWidgetBase
from core.models.widgets.selects import CheckboxModel, SelectModel, RadioModel, MultiSelectModel


class TestSelect(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'checkbox': {
            'checked': '✓ Checked',
            'unchecked': 'Unchecked',
            'default': False,
            'id': 'check'
        }}, CheckboxModel, Checkbox),
        ({'select': {
            'format': '{item.name} ({item.id})',
            'id': 'sel',
            'items': 'get_data',
            'item_id_getter': 'func_test',
            'on_click': 'func_test'
        }}, SelectModel, Select),
        ({'select': {
            'text': '{item.name} ({item.id})',
            'id': 'sel',
            'items': 'get_data',
            'item_id_getter': 'func_test',
            'on_click': 'func_test'
        }}, SelectModel, Select),
        ({'radio': {
            'checked': '🔘 {item.name}',
            'unchecked': '⚪️ {item.name}',
            'id': 'radio',
            'items': 'get_data',
            'item_id_getter': 'func_test'
        }}, RadioModel, Radio),
        ({'multi_select': {
                'checked': '✓ {item.name}',
                'unchecked': '{item.name}',
                'id': 'multi',
                'items': 'func_test',
                'item_id_getter': 'func_test'
        }}, MultiSelectModel, Multiselect),
    ])
    def test_select(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.model_parser_class.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
