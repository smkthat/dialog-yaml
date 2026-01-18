"""Unit tests for Select widget models."""

import pytest

from dialog_yml.models.widgets.selects.select import (
    SelectModel,
    CheckboxModel,
    RadioModel,
    MultiSelectModel,
)
from dialog_yml.models.funcs.func import function_registry


class TestSelectModel:
    """Unit tests for SelectModel functionality."""

    def test_select_model_creation_basic(self):
        """Test basic SelectModel creation."""

        # Register test function
        def click_handler(x=None):
            return x

        function_registry.register(click_handler, "func")

        # Given
        widget_data = {
            "id": "test_select",
            "items": ["item1", "item2", "item3"],
            "item_id_getter": 0,
            "text": "{item}",
        }

        # When
        select_model = SelectModel.to_model(widget_data)

        # Then
        assert select_model.id == "test_select"
        assert select_model.items == ["item1", "item2", "item3"]
        assert select_model.item_id_getter == 0

    def test_select_model_creation_with_on_click(self):
        """Test SelectModel creation with on_click function."""

        # Register test functions
        def click_handler(x=None):
            return x

        function_registry.register(click_handler, "func")

        # Given
        widget_data = {
            "id": "test_select",
            "items": ["item1", "item2"],
            "item_id_getter": "id",
            "on_click": "click_handler",
            "text": "{item}",
        }

        # When
        select_model = SelectModel.to_model(widget_data)

        # Then
        assert select_model.id == "test_select"
        assert select_model.items == ["item1", "item2"]
        assert select_model.item_id_getter == "id"
        assert select_model.on_click.name == "click_handler"

    @pytest.mark.parametrize(
        "widget_data",
        [
            (
                {
                    "id": "sel1",
                    "items": ["a", "b"],
                    "item_id_getter": 0,
                    "text": "{item}",
                }
            ),
        ],
    )
    def test_select_model_creation_various_configs(self, widget_data):
        """Test SelectModel creation with various configurations."""

        # Register test function
        def click_handler(x=None):
            return x

        function_registry.register(click_handler, "func")

        # When
        select_model = SelectModel.to_model(widget_data)

        # Then
        assert select_model.id == widget_data["id"]
        assert select_model.items == widget_data["items"]
        assert select_model.item_id_getter == widget_data["item_id_getter"]

    def test_select_model_to_object(self):
        """Test converting SelectModel to object."""

        # Register test function
        def click_handler(x=None):
            return x

        function_registry.register(click_handler, "func")

        # Given
        widget_data = {
            "id": "test_select",
            "items": ["item1", "item2"],
            "item_id_getter": 0,
            "text": "{item}",
        }
        select_model = SelectModel.to_model(widget_data)

        # When
        widget_obj = select_model.to_object()

        # Then
        # Just verify that it returns an object
        assert widget_obj is not None


class TestCheckboxModel:
    """Unit tests for CheckboxModel functionality."""

    def test_checkbox_model_creation_basic(self):
        """Test basic CheckboxModel creation."""
        # Given
        widget_data = {
            "id": "test_checkbox",
            "checked": {"val": "[x] Selected"},
            "unchecked": {"val": "[ ] Not selected"},
            "default": True,
        }

        # When
        checkbox_model = CheckboxModel.to_model(widget_data)

        # Then
        assert checkbox_model.id == "test_checkbox"
        assert checkbox_model.checked.val == "[x] Selected"
        assert checkbox_model.unchecked.val == "[ ] Not selected"
        assert checkbox_model.default is True

    def test_checkbox_model_with_on_state_changed(self):
        """Test CheckboxModel creation with on_state_changed."""

        # Register test function
        def state_change_handler(x=None):
            return x

        function_registry.register(state_change_handler, "func")

        # Given
        widget_data = {
            "id": "test_checkbox",
            "on_state_changed": "state_change_handler",
            "default": False,
        }

        # When
        checkbox_model = CheckboxModel.to_model(widget_data)

        # Then
        assert checkbox_model.id == "test_checkbox"
        assert checkbox_model.on_state_changed.name == "state_change_handler"
        assert checkbox_model.default is False

    @pytest.mark.parametrize(
        "widget_data",
        [
            (
                {
                    "id": "chk1",
                    "checked": {"val": "[x]"},
                    "unchecked": {"val": "[ ]"},
                    "default": True,
                }
            ),
        ],
    )
    def test_checkbox_model_creation_various_configs(self, widget_data):
        """Test CheckboxModel creation with various configurations."""
        # When
        checkbox_model = CheckboxModel.to_model(widget_data)

        # Then
        assert checkbox_model.id == widget_data["id"]
        if "default" in widget_data:
            assert checkbox_model.default == widget_data["default"]


class TestRadioModel:
    """Unit tests for RadioModel functionality."""

    def test_radio_model_creation_basic(self):
        """Test basic RadioModel creation."""
        # Given
        widget_data = {
            "id": "test_radio",
            "items": ["option1", "option2"],
            "item_id_getter": "id",
            "checked": {"val": "✓ {item}"},
            "unchecked": {"val": "{item}"},
        }

        # When
        radio_model = RadioModel.to_model(widget_data)

        # Then
        assert radio_model.id == "test_radio"
        assert radio_model.items == ["option1", "option2"]
        assert radio_model.item_id_getter == "id"
        assert radio_model.checked.val == "✓ {item}"
        assert radio_model.unchecked.val == "{item}"

    def test_radio_model_with_on_state_changed(self):
        """Test RadioModel creation with on_state_changed."""

        # Register test function
        def change_handler(x=None):
            return x

        function_registry.register(change_handler, "func")

        # Given
        widget_data = {
            "id": "test_radio",
            "items": ["option1", "option2"],
            "item_id_getter": 0,
            "on_state_changed": "change_handler",
        }

        # When
        radio_model = RadioModel.to_model(widget_data)

        # Then
        assert radio_model.id == "test_radio"
        assert radio_model.items == ["option1", "option2"]
        assert radio_model.item_id_getter == 0
        assert radio_model.on_state_changed.name == "change_handler"

    @pytest.mark.parametrize(
        "widget_data",
        [
            (
                {
                    "id": "rad1",
                    "items": ["a", "b"],
                    "item_id_getter": "id",
                    "checked": {"val": "✓ {item}"},
                    "unchecked": {"val": "{item}"},
                }
            ),
        ],
    )
    def test_radio_model_creation_various_configs(self, widget_data):
        """Test RadioModel creation with various configurations."""
        # When
        radio_model = RadioModel.to_model(widget_data)

        # Then
        assert radio_model.id == widget_data["id"]
        assert radio_model.items == widget_data["items"]
        assert radio_model.item_id_getter == widget_data["item_id_getter"]


class TestMultiSelectModel:
    """Unit tests for MultiSelectModel functionality."""

    def test_multiselect_model_creation_basic(self):
        """Test basic MultiSelectModel creation."""

        # Register test functions
        def change_handler(x=None):
            return x

        def click_handler(x=None):
            return x

        function_registry.register(change_handler, "func")
        function_registry.register(click_handler, "func")

        # Given
        widget_data = {
            "id": "test_multiselect",
            "items": ["item1", "item2", "item3"],
            "item_id_getter": 0,
            "on_state_changed": "change_handler",
            "on_click": "click_handler",
            "min_selected": 1,
            "max_selected": 2,
        }

        # When
        multiselect_model = MultiSelectModel.to_model(widget_data)

        # Then
        assert multiselect_model.id == "test_multiselect"
        assert multiselect_model.items == ["item1", "item2", "item3"]
        assert multiselect_model.item_id_getter == 0
        assert multiselect_model.on_state_changed.name == "change_handler"
        assert multiselect_model.on_click.name == "click_handler"
        assert multiselect_model.min_selected == 1
        assert multiselect_model.max_selected == 2

    @pytest.mark.parametrize(
        "widget_data",
        [
            (
                {
                    "id": "ms1",
                    "items": ["a", "b"],
                    "item_id_getter": "id",
                    "min_selected": 0,
                    "max_selected": 1,
                }
            ),
        ],
    )
    def test_multiselect_model_creation_various_configs(self, widget_data):
        """Test MultiSelectModel creation with various configurations."""
        # When
        multiselect_model = MultiSelectModel.to_model(widget_data)

        # Then
        assert multiselect_model.id == widget_data["id"]
        assert multiselect_model.items == widget_data["items"]
        assert multiselect_model.item_id_getter == widget_data["item_id_getter"]
        assert multiselect_model.min_selected == widget_data["min_selected"]
        assert multiselect_model.max_selected == widget_data["max_selected"]
