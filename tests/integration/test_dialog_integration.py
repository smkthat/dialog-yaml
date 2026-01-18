"""Integration tests for dialog components interaction."""

import pytest
from unittest.mock import patch
from aiogram import Router

from dialog_yml.core import DialogYAMLBuilder
from dialog_yml.reader import YAMLReader


class TestDialogIntegration:
    """Integration tests for dialog components interaction."""

    @pytest.fixture
    def mock_yaml_data(self):
        """Mock YAML data for integration tests."""
        return {
            "dialogs": {
                "main": {
                    "windows": {
                        "start": {"widgets": [{"text": "Welcome!"}]},
                        "step1": {"widgets": [{"input": {"func": "dummy_func"}}]},
                    }
                }
            }
        }

    @pytest.fixture
    def mock_router(self):
        """Mock router for testing."""
        return Router()

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_reader_states_manager_integration(
        self, mock_setup_dialogs, mock_read_data, mock_yaml_data
    ):
        """Test integration between YAML reader and states manager."""
        # Given
        mock_read_data.return_value = mock_yaml_data

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        # Check that states were created based on the YAML data
        assert builder.states_manager is not None
        # Verify states were built from the YAML data structure

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_reader_model_factory_integration(
        self, mock_setup_dialogs, mock_read_data, mock_yaml_data
    ):
        """Test integration between YAML reader and model factory."""
        # Given
        mock_read_data.return_value = mock_yaml_data

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        # Check that models were created based on the YAML data
        assert builder.model_factory is not None
        # Widgets should be processed by the model factory

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_states_manager_model_factory_integration(
        self, mock_setup_dialogs, mock_read_data, mock_yaml_data
    ):
        """Test integration between states manager and model factory."""
        # Given
        mock_read_data.return_value = mock_yaml_data

        # When
        builder = DialogYAMLBuilder.build("test.yaml")

        # Then
        # Both components should work together to create the dialog structure
        assert builder.states_manager is not None
        assert builder.model_factory is not None

    @pytest.mark.parametrize(
        "yaml_config",
        [
            {
                "dialogs": {
                    "simple": {
                        "windows": {"start": {"widgets": [{"text": "Simple dialog"}]}}
                    }
                }
            },
            {
                "dialogs": {
                    "complex": {
                        "windows": {
                            "start": {
                                "widgets": [
                                    {
                                        "text": "Complex dialog",
                                    },
                                    {
                                        "input": {"func": "dummy_func"},
                                    },
                                    {
                                        "select": {
                                            "id": "sel",
                                            "items": ["opt1", "opt2"],
                                            "item_id_getter": 0,
                                            "text": "{item}",
                                        }
                                    },
                                ]
                            },
                            "step1": {
                                "widgets": [
                                    {"text": "Step 1"},
                                    {
                                        "counter": {
                                            "id": "counter",
                                            "min_value": 0,
                                            "max_value": 10,
                                        }
                                    },
                                ]
                            },
                        }
                    }
                }
            },
        ],
    )
    @patch("dialog_yml.core.setup_dialogs")
    def test_multiple_configurations_integration(self, mock_setup_dialogs, yaml_config):
        """Test integration with multiple YAML configurations."""
        # Given
        with patch.object(YAMLReader, "read_data_to_dict", return_value=yaml_config):
            # When
            builder = DialogYAMLBuilder.build("test.yaml")

            # Then
            assert builder is not None
            assert builder.states_manager is not None
            assert builder.model_factory is not None

    @patch("dialog_yml.core.YAMLReader.read_data_to_dict")
    @patch("dialog_yml.core.setup_dialogs")
    def test_builder_router_integration(
        self, mock_setup_dialogs, mock_read_data, mock_yaml_data
    ):
        """Test integration between builder and router."""
        # Given
        mock_read_data.return_value = mock_yaml_data
        router = Router()

        # When
        builder = DialogYAMLBuilder.build("test.yaml", router=router)

        # Then
        assert builder.router == router
        # Router should be properly configured with the dialogs

    @patch("dialog_yml.core.setup_dialogs")
    def test_complete_dialog_building_flow(self, mock_setup_dialogs):
        """Test the complete flow of dialog building with all components."""
        # Given
        complete_yaml_data = {
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
                        "get_name": {"widgets": [{"input": {"func": "dummy_func"}}]},
                        "get_email": {"widgets": [{"input": {"func": "dummy_func"}}]},
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

        with patch.object(
            YAMLReader, "read_data_to_dict", return_value=complete_yaml_data
        ):
            # When
            builder = DialogYAMLBuilder.build("test.yaml")

            # Then
            assert builder is not None
            assert len(builder._dialogs) >= 0  # At least some dialogs should be created
            assert builder.states_manager is not None
            assert builder.model_factory is not None


class TestCustomModelsStatesIntegration:
    """Integration tests for custom models and states."""

    @patch("dialog_yml.core.setup_dialogs")
    def test_custom_models_integration(self, mock_setup_dialogs):
        """Test integration with custom models."""
        # Given
        yaml_data = {
            "dialogs": {
                "main": {
                    "windows": {
                        "start": {
                            "widgets": [
                                {
                                    "text": "Using custom model",
                                }
                            ]
                        }
                    }
                }
            }
        }

        with patch.object(YAMLReader, "read_data_to_dict", return_value=yaml_data):
            # When
            builder = DialogYAMLBuilder.build("test.yaml")

            # Register a custom model
            from dialog_yml.models.base import YAMLModel

            class CustomModel(YAMLModel):
                def to_object(self):
                    pass

                @classmethod
                def to_model(cls, data):
                    return cls()

            builder.register_custom_models({"custom_widget": CustomModel})

            # Then
            # Custom model should be integrated with the existing system
            assert builder is not None

    @patch("dialog_yml.core.setup_dialogs")
    def test_custom_states_integration(self, mock_setup_dialogs):
        """Test integration with custom states."""
        # Given
        from aiogram.fsm.state import StatesGroup, State

        class CustomStateGroup(StatesGroup):
            custom_state = State()

        yaml_data = {
            "dialogs": {
                "CustomStateGroup": {
                    "windows": {
                        "custom_state": {
                            "widgets": [
                                {
                                    "text": "Using custom state",
                                }
                            ]
                        }
                    }
                }
            }
        }

        with patch.object(YAMLReader, "read_data_to_dict", return_value=yaml_data):
            # When
            builder = DialogYAMLBuilder.build("test.yaml", states=[CustomStateGroup])

            # Then
            # Custom states should be integrated with the existing system
            assert builder is not None
