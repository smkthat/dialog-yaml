import pytest
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List

from conftest import TestWidgetBase
from core.models.widgets.texts import TextModel, FormatModel, MultiTextModel, CaseModel, ListModel


class TestText(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'text': 'Test text {name}'},
         TextModel, Const),
        ({'text': {
            'val': 'Test text {name}',
            'when': 'func_test'
        }}, TextModel, Const),
        ({'text': {
            'val': 'Test text {name}',
            'formatted': True,
            'when': 'func_test'
        }}, TextModel, Format),
        ({'format': 'Test text {name}'},
         FormatModel, Format),
        ({'format': {
            'val': 'Test text {name}',
            'when': 'func_test'
        }}, FormatModel, Format),
        ({'case': {
            'texts': {True: 'Enabled', False: 'Disabled'},
            'selector': 'selector_key'
        }}, CaseModel, Case),
        ({'case': {
            'texts': {True: 'Enabled', False: 'Disabled'},
            'selector': {'func': 'func_test'}
        }}, CaseModel, Case),
        ({'multi': {'texts': [
            {'format': 'Test text {name}'},
            {'text': 'Test text {name}'}
        ]}}, MultiTextModel, Multi),
        ({'list': {
            'field': {'val': '+ {item.name} - {item.id}', 'formatted': True},
            'items': 'get_data',
            'when': 'func_test'
        }}, ListModel, List),
        ({'list': {
            'field': {'val': '+ {item.name} - {item.id}', 'formatted': True},
            'items': ['a', 'b', 'c', 'd'],
            'when': 'func_test'
        }}, ListModel, List),
    ])
    def test_text(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.model_parser_class.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
