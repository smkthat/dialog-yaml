import pytest
from aiogram_dialog.widgets.kbd import Calendar

from dialog_yml.models.widgets.calendars import CalendarModel
from tests.models.widgets.conftest import TestWidgetBase


class TestCalendar(TestWidgetBase):
    @pytest.mark.parametrize(
        "input_data, expected_model_cls, expected_widget_cls",
        [
            (
                {"calendar": {"id": "cal", "on_click": "test_func"}},
                CalendarModel,
                Calendar,
            ),
        ],
    )
    def test_calendar(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
