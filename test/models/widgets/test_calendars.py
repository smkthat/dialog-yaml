import pytest
from aiogram_dialog.widgets.kbd import Calendar

from core.models.widgets.calendars import CalendarModel
from test.models.widgets.conftest import TestWidgetBase


class TestCalendar(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'calendar': {'id': 'cal', 'on_click': 'test_func'}},
         CalendarModel, Calendar),
    ])
    def test_calendar(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
