import pytest
from unittest.mock import patch
from aiogram import Router

from dialog_yml.core import DialogYAMLBuilder
from dialog_yml.models.base import YAMLModel


class TestDialogYAMLBuilder:
    """Unit tests for DialogYAMLBuilder functionality."""

    @pytest.fixture
    def builder(self) -> DialogYAMLBuilder:
        """Fixture for DialogYAMLBuilder instance."""
        return DialogYAMLBuilder("test.yaml")

    def test_initialization(self):
        """Test DialogYAMLBuilder initialization."""
        # Given/When
        builder = DialogYAMLBuilder("test.yaml")

        # Then
        assert builder.yaml_file_name == "test.yaml"
        assert builder.yaml_dir_path == ""
        assert builder.funcs_registry is not None
        assert builder.states_manager is not None
        assert builder.model_factory is not None

    def test_initialization_with_custom_params(self):
        """Test DialogYAMLBuilder initialization with custom parameters."""
        # Given/When
        router = Router()
        builder = DialogYAMLBuilder("custom.yaml", "/path/to/dir", router)

        # Then
        assert builder.yaml_file_name == "custom.yaml"
        assert builder.yaml_dir_path == "/path/to/dir"
        assert builder.router == router

    def test_router_property(self):
        """Test router property access."""
        # Given
        router = Router()
        builder = DialogYAMLBuilder("test.yaml", "", router)

        # When
        retrieved_router = builder.router

        # Then
        assert retrieved_router == router

    @patch("dialog_yml.core.setup_dialogs")
    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    def test_build_method_success(self, mock_read_data, mock_setup_dialogs):
        """Test building dialog from valid configuration using class method."""
        # Given
        mock_read_data.return_value = {
            "dialogs": {
                "main": {"windows": {"start": {"widgets": [{"text": "Welcome!"}]}}}
            }
        }

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        assert isinstance(builder, DialogYAMLBuilder)
        assert builder.yaml_file_name == "test.yaml"

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    def test_build_with_empty_data_raises_exception(self, mock_read_data):
        """Test building with empty data raises exception."""
        # Given
        mock_read_data.return_value = {}

        # When/Then
        with pytest.raises(Exception):  # Should raise DialogYamlException
            DialogYAMLBuilder.build("test.yaml")

    @pytest.mark.parametrize(
        "yaml_tag,replace_existing",
        [
            ("my_custom_widget", False),
            ("another_widget", True),
        ],
    )
    def test_register_custom_models(self, yaml_tag, replace_existing):
        """Test registering custom models."""
        # Given
        builder = DialogYAMLBuilder("test.yaml")

        class CustomModel(YAMLModel):
            def to_object(self):
                pass

            @classmethod
            def to_model(cls, data):
                return cls()

        custom_models = {yaml_tag: CustomModel}

        # When
        builder.register_custom_models(custom_models, replace_existing)

        # Then
        # The model should be registered in the factory

    def test_register_custom_models_empty_dict(self):
        """Test registering empty custom models dict does nothing."""
        # Given
        builder = DialogYAMLBuilder("test.yaml")
        custom_models = {}

        # When
        builder.register_custom_models(custom_models)

        # Then
        # No exception should occur, and nothing should be registered

    def test_register_custom_states_empty_list(self):
        """Test registering empty custom states list does nothing."""
        # Given
        builder = DialogYAMLBuilder("test.yaml")
        custom_states = []

        # When
        builder.register_custom_states(custom_states)

        # Then
        # No exception should occur, and nothing should be registered

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    def test_check_yaml_data_base_structure_valid(self, mock_read_data):
        """Test checking valid YAML data structure."""
        # Given
        valid_data = {"dialogs": {"main": {"windows": {"start": {"widgets": []}}}}}
        mock_read_data.return_value = valid_data
        _ = DialogYAMLBuilder("test.yaml")

        # When
        result = DialogYAMLBuilder.check_yaml_data_base_structure(valid_data)

        # Then
        assert result is True

    @pytest.mark.parametrize(
        "invalid_data",
        [
            ({"dialogs": {}}),  # Empty dialogs
            ({"dialogs": {"main": {"windows": {}}}}),  # Empty windows
        ],
    )
    def test_check_yaml_data_base_structure_invalid_empty(self, invalid_data):
        """Test checking invalid empty YAML data structure raises exception."""
        # Given/When/Then
        with pytest.raises(Exception):  # Should raise InvalidTagName
            DialogYAMLBuilder.check_yaml_data_base_structure(invalid_data)

    @pytest.mark.parametrize(
        "invalid_data",
        [
            ({}),  # No dialogs tag
            ({"dialogs": {"main": {}}}),  # No windows tag
            ({"dialogs": {"main": {"windows": {"start": {}}}}}),  # No widgets tag
        ],
    )
    def test_check_yaml_data_base_structure_invalid(self, invalid_data):
        """Test checking invalid YAML data structure raises exception."""
        # Given/When/Then
        with pytest.raises(Exception):  # Could raise various exceptions
            DialogYAMLBuilder.check_yaml_data_base_structure(invalid_data)


class TestDialogYAMLBuilderIntegration:
    """Integration tests for DialogYAMLBuilder with real components."""

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_full_build_process_with_real_components(
        self, mock_setup_dialogs, mock_read_data
    ):
        """Test the full build process with real components (integration)."""
        # Given
        mock_read_data.return_value = {
            "dialogs": {
                "main": {"windows": {"start": {"widgets": [{"text": "Welcome!"}]}}}
            }
        }

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        assert isinstance(builder, DialogYAMLBuilder)
        assert builder.states_manager is not None
        assert builder.model_factory is not None

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_build_with_complex_configuration(self, mock_setup_dialogs, mock_read_data):
        """Test building with a more complex configuration."""
        # Given
        complex_data = {
            "dialogs": {
                "registration": {
                    "windows": {
                        "welcome": {
                            "widgets": [
                                {
                                    "text": "Welcome to registration!",
                                }
                            ]
                        },
                        "get_name": {
                            "widgets": [
                                {
                                    "input": {"func": "dummy_func"},
                                }
                            ]
                        },
                        "confirm": {
                            "widgets": [
                                {
                                    "select": {
                                        "id": "sel",
                                        "items": ["Yes", "No"],
                                        "item_id_getter": 0,
                                        "text": "{item}",
                                    }
                                }
                            ]
                        },
                    }
                }
            }
        }
        mock_read_data.return_value = complex_data

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        assert isinstance(builder, DialogYAMLBuilder)
        # Should have processed all the dialog windows
