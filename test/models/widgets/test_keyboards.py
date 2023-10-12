import pytest
from aiogram_dialog.widgets.kbd import (
    Url,
    Button,
    SwitchTo,
    Start,
    Next,
    Back,
    Cancel,
    Group,
    ScrollingGroup,
)

from core.models.widgets.kbd import (
    UrlButtonModel,
    CallbackButtonModel,
    SwitchToModel,
    StartModel,
    NextModel,
    BackModel,
    CancelModel,
    GroupKeyboardModel,
    RowKeyboardModel,
    ColumnKeyboardModel,
    ScrollingGroupKeyboardModel,
)
from test.models.widgets.conftest import TestWidgetBase


class TestKeyboard(TestWidgetBase):
    @pytest.mark.parametrize(
        "input_data, expected_model_cls, expected_widget_cls",
        [
            (
                {
                    "url": {
                        "text": "Url button text",
                        "uri": "https://example.com",
                    }
                },
                UrlButtonModel,
                Url,
            ),
            (
                {
                    "callback": {
                        "id": "callback",
                        "text": "Callback with funcs",
                        "on_click": {"name": "test_getter", "data": {"key": "value"}},
                        "pre_on_click": "test_func",
                        "after_on_click": "test_func",
                        "notify": {
                            "func": "test_notify",
                            "val": "This is alert notify with 3 sec delay",
                            "show_alert": True,
                            "delay": 3,
                        },
                    }
                },
                CallbackButtonModel,
                Button,
            ),
            (
                {
                    "switch_to": {
                        "id": "switch",
                        "text": "Switch to",
                        "state": "group1:state1",
                    }
                },
                SwitchToModel,
                SwitchTo,
            ),
            (
                {
                    "start": {
                        "id": "start",
                        "text": "Start",
                        "state": "group1:state1",
                        "mode": "NORMAL",
                    }
                },
                StartModel,
                Start,
            ),
            ({"next": "Next"}, NextModel, Next),
            ({"back": "Back"}, BackModel, Back),
            ({"cancel": "Cancel"}, CancelModel, Cancel),
            (
                {
                    "group": {
                        "width": 2,
                        "buttons": [
                            {
                                "start": {
                                    "id": "start",
                                    "text": "Start",
                                    "state": "group1:state1",
                                }
                            },
                            {"next": {}},
                            {"back": {}},
                            {"cancel": {}},
                        ],
                    }
                },
                GroupKeyboardModel,
                Group,
            ),
            (
                {
                    "row": {
                        "buttons": [
                            {
                                "start": {
                                    "id": "start",
                                    "text": "Start",
                                    "state": "group1:state1",
                                }
                            },
                            {"next": {}},
                            {"back": {}},
                            {"cancel": {}},
                        ]
                    }
                },
                RowKeyboardModel,
                Group,
            ),
            (
                {
                    "column": {
                        "buttons": [
                            {
                                "start": {
                                    "id": "start",
                                    "text": "Start",
                                    "state": "group1:state1",
                                }
                            },
                            {"next": {}},
                            {"back": {}},
                            {"cancel": {}},
                        ]
                    }
                },
                ColumnKeyboardModel,
                Group,
            ),
            (
                {
                    "scrolling_group": {
                        "width": 1,
                        "height": 2,
                        "hide_pager": True,
                        "id": "scrolling_group",
                        "buttons": [
                            {
                                "start": {
                                    "id": "start",
                                    "text": "Start",
                                    "state": "group1:state1",
                                }
                            },
                            {"next": {}},
                            {"back": {}},
                            {"cancel": {}},
                        ],
                    }
                },
                ScrollingGroupKeyboardModel,
                ScrollingGroup,
            ),
        ],
    )
    def test_keyboard(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
