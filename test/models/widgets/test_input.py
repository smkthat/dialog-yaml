import pytest
from aiogram_dialog.widgets.input import MessageInput

from core.models.widgets.inputs import MessageInputModel
from test.models.widgets.conftest import TestWidgetBase


class TestInput(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'input': {
            'func': 'test_func',
            'content_types': 'text'
        }},
         MessageInputModel, MessageInput),
        ({'input': {
            'func': 'test_func',
            'content_types': ['text', 'photo']
        }},
         MessageInputModel, MessageInput),
    ])
    def test_input(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
