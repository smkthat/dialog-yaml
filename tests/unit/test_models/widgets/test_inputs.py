"""Unit tests for MessageInput widget model."""

import pytest
from aiogram.enums import ContentType

from dialog_yml.models.widgets.inputs.input import MessageInputModel
from dialog_yml.models.funcs.func import function_registry


class TestMessageInputModel:
    """Unit tests for MessageInputModel functionality."""

    def test_message_input_model_creation_basic(self):
        """Test basic MessageInputModel creation."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {"func": "test_function"}

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"

    def test_message_input_model_creation_with_filter(self):
        """Test MessageInputModel creation with filter."""

        # Register test functions
        def test_function(x=None):
            return x

        def test_filter(x=None):
            return x

        function_registry.register(test_function, "func")
        function_registry.register(test_filter, "func")

        # Given
        widget_data = {"func": "test_function", "filter": "test_filter"}

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"
        assert input_model.filter.name == "test_filter"

    def test_message_input_model_creation_with_content_types(self):
        """Test MessageInputModel creation with content types."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {
            "func": "test_function",
            "content_types": [ContentType.TEXT, ContentType.PHOTO],
        }

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"
        assert ContentType.TEXT in input_model.content_types
        assert ContentType.PHOTO in input_model.content_types

    @pytest.mark.parametrize(
        "widget_data",
        [
            ({"func": "test_function"}),
        ],
    )
    def test_message_input_model_creation_various_configs(self, widget_data):
        """Test MessageInputModel creation with various configurations."""

        # Register test function
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == widget_data["func"]

    def test_message_input_model_to_object(self):
        """Test converting MessageInputModel to object."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {"func": "test_function"}
        input_model = MessageInputModel.to_model(widget_data)

        # When
        widget_obj = input_model.to_object()

        # Then
        # Just verify that it returns an object (in real implementation it would return an actual MessageInput)
        assert widget_obj is not None

    def test_content_types_validation_single_string(self):
        """Test content types validation with single string."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {"func": "test_function", "content_types": "text"}

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"
        assert ContentType.TEXT in input_model.content_types

    def test_content_types_validation_list_of_strings(self):
        """Test content types validation with list of strings."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {
            "func": "test_function",
            "content_types": ["text", "photo"],
        }

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"
        assert ContentType.TEXT in input_model.content_types
        assert ContentType.PHOTO in input_model.content_types

    def test_content_types_validation_empty(self):
        """Test content types validation with empty value."""

        # Register a test function first
        def test_function(x=None):
            return x

        function_registry.register(test_function, "func")

        # Given
        widget_data = {"func": "test_function", "content_types": []}

        # When
        input_model = MessageInputModel.to_model(widget_data)

        # Then
        assert input_model.func.name == "test_function"
        # Default value should be [ContentType.ANY]
        assert input_model.content_types == [ContentType.ANY]
