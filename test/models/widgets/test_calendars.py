import pytest
from aiogram_dialog.widgets.kbd import Calendar

from conftest import TestWidgetBase
from core.models.widgets.calendars import CalendarModel


class TestCalendar(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'calendar': {'id': 'cal', 'on_click': 'func_test'}},
         CalendarModel, Calendar),
    ])
    def test_calendar(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.model_parser_class.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
