import pytest
from aiogram_dialog.widgets.kbd import Counter
from aiogram_dialog.widgets.text import Progress

from conftest import TestWidgetBase
from core.models.widgets.counters import ProgressModel, CounterModel


class TestCounters(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'progress': {
            'field': 'progress',
            'width': 10,
            'filled': '█',
            'empty': '░️'
        }},
         ProgressModel, Progress),
        ({'counter': {
            'id': 'counter',
            'default': 0,
            'max_value': 10,
            'on_text_click': 'func_test'
        }},
         CounterModel, Counter),
    ])
    def test_counters(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.model_parser_class.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
