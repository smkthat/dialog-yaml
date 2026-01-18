import pytest
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List

from dialog_yml.models.widgets.texts.text import (
    TextModel,
    FormatModel,
    MultiTextModel,
    CaseModel,
    ListModel,
)
from tests.models.widgets.conftest import TestWidgetBase


class TestText(TestWidgetBase):
    @pytest.mark.parametrize(
        "input_data, expected_model_cls, expected_widget_cls",
        [
            ({"text": "Test text {name}"}, TextModel, Const),
            (
                {"text": {"val": "Test text {name}", "when": "test_func"}},
                TextModel,
                Const,
            ),
            (
                {
                    "text": {
                        "val": "Test text {name}",
                        "formatted": True,
                        "when": "test_func",
                    }
                },
                TextModel,
                Format,
            ),
            ({"format": "Test text {name}"}, FormatModel, Format),
            (
                {"format": {"val": "Test text {name}", "when": "test_func"}},
                FormatModel,
                Format,
            ),
            (
                {
                    "case": {
                        "texts": {True: "Enabled", False: "Disabled"},
                        "selector": "selector_key",
                    }
                },
                CaseModel,
                Case,
            ),
            (
                {
                    "case": {
                        "texts": {True: "Enabled", False: "Disabled"},
                        "selector": {"func": "test_func"},
                    }
                },
                CaseModel,
                Case,
            ),
            (
                {
                    "multi": {
                        "texts": [
                            {"format": "Test text {name}"},
                            {"text": "Test text {name}"},
                        ]
                    }
                },
                MultiTextModel,
                Multi,
            ),
            (
                {
                    "list": {
                        "field": {
                            "val": "+ {item.name} - {item.id}",
                            "formatted": True,
                        },
                        "items": "get_data",
                        "when": "test_func",
                    }
                },
                ListModel,
                List,
            ),
            (
                {
                    "list": {
                        "field": {
                            "val": "+ {item.name} - {item.id}",
                            "formatted": True,
                        },
                        "items": ["a", "b", "c", "d"],
                        "when": "test_func",
                    }
                },
                ListModel,
                List,
            ),
        ],
    )
    def test_text(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
