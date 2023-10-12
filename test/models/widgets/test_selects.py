import pytest
from aiogram_dialog.widgets.kbd import Checkbox, Select, Radio, Multiselect

from core.models.widgets.selects import (
    CheckboxModel,
    SelectModel,
    RadioModel,
    MultiSelectModel,
)
from test.models.widgets.conftest import TestWidgetBase


class TestSelect(TestWidgetBase):
    @pytest.mark.parametrize(
        "input_data, expected_model_cls, expected_widget_cls",
        [
            (
                {
                    "checkbox": {
                        "checked": "✓ Checked",
                        "unchecked": "Unchecked",
                        "default": False,
                        "id": "check",
                    }
                },
                CheckboxModel,
                Checkbox,
            ),
            (
                {
                    "select": {
                        "format": "{item.name} ({item.id})",
                        "id": "sel",
                        "items": "get_data",
                        "item_id_getter": "test_func",
                        "on_click": "test_func",
                    }
                },
                SelectModel,
                Select,
            ),
            (
                {
                    "select": {
                        "text": "{item.name} ({item.id})",
                        "id": "sel",
                        "items": "get_data",
                        "item_id_getter": "test_func",
                        "on_click": "test_func",
                    }
                },
                SelectModel,
                Select,
            ),
            (
                {
                    "radio": {
                        "checked": "🔘 {item.name}",
                        "unchecked": "⚪️ {item.name}",
                        "id": "radio",
                        "items": "get_data",
                        "item_id_getter": "test_func",
                    }
                },
                RadioModel,
                Radio,
            ),
            (
                {
                    "multi_select": {
                        "checked": "✓ {item.name}",
                        "unchecked": "{item.name}",
                        "id": "multi",
                        "items": "test_func",
                        "item_id_getter": "test_func",
                    }
                },
                MultiSelectModel,
                Multiselect,
            ),
        ],
    )
    def test_select(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
