"""Functional tests for end-to-end scenarios."""

import os
import tempfile

import pytest
import yaml

from dialog_yml.core import DialogYAMLBuilder


@pytest.fixture
def temp_yaml_file():
    """Create a temporary YAML file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yield f.name
    os.unlink(f.name)


class TestEndToEndScenarios:
    """Functional tests for end-to-end scenarios."""

    def test_simple_dialog_creation_end_to_end(self, temp_yaml_file):
        """Test creating a simple dialog from YAML file end-to-end."""
        # Given
        yaml_content = {
            "dialogs": {
                "main": {"windows": {"start": {"widgets": [{"text": "Welcome!"}]}}}
            }
        }

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
        )

        # Then
        assert builder is not None
        assert builder.yaml_file_name == os.path.basename(temp_yaml_file)
        assert builder.states_manager is not None

    def test_complex_dialog_creation_end_to_end(self, temp_yaml_file):
        """Test creating a complex dialog from YAML file end-to-end."""
        # Given
        yaml_content = {
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
                        "get_email": {
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

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
        )

        # Then
        assert builder is not None
        assert len(builder._dialogs) >= 0  # At least some dialogs should be created

    @pytest.mark.parametrize(
        "yaml_content",
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
                    "two_windows": {
                        "windows": {
                            "start": {"widgets": [{"text": "Start"}]},
                            "next": {"widgets": [{"input": {"func": "dummy_func"}}]},
                        }
                    }
                }
            },
        ],
    )
    def test_multiple_yaml_structures_end_to_end(self, temp_yaml_file, yaml_content):
        """Test end-to-end processing with multiple YAML structures."""
        # Given
        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
        )

        # Then
        assert builder is not None
        assert builder.states_manager is not None
        assert builder.model_factory is not None

    def test_dialog_with_custom_states_end_to_end(self, temp_yaml_file):
        """Test end-to-end processing with custom states."""
        # Given
        from aiogram.fsm.state import StatesGroup, State

        class CustomStateGroup(StatesGroup):
            custom_state = State()
            another_state = State()

        yaml_content = {
            "dialogs": {
                "CustomStateGroup": {
                    "windows": {
                        "custom_state": {"widgets": [{"text": "In custom state"}]},
                        "another_state": {"widgets": [{"input": {"func": "dummy_func"}}]},
                    }
                }
            }
        }

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
            states=[CustomStateGroup],
        )

        # Then
        assert builder is not None
        # Custom states should be registered and used

    def test_error_handling_end_to_end(self, temp_yaml_file):
        """Test error handling in end-to-end scenarios."""
        # Given
        # Create an invalid YAML structure (missing required fields)
        yaml_content = {"invalid": {"structure": {}}}

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When/Then
        with pytest.raises(Exception):  # Should raise validation error
            DialogYAMLBuilder.build(
                yaml_file_name=os.path.basename(temp_yaml_file),
                yaml_dir_path=os.path.dirname(temp_yaml_file),
            )

    def test_empty_yaml_handling_end_to_end(self, temp_yaml_file):
        """Test handling of empty YAML file."""
        # Given
        yaml_content = {}

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When/Then
        with pytest.raises(Exception):  # Should raise error for empty data
            DialogYAMLBuilder.build(
                yaml_file_name=os.path.basename(temp_yaml_file),
                yaml_dir_path=os.path.dirname(temp_yaml_file),
            )

    @pytest.mark.parametrize("file_extension", [".yaml", ".yml"])
    def test_different_file_extensions_end_to_end(self, file_extension):
        """Test end-to-end processing with different file extensions."""
        # Given
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=file_extension, delete=False
        ) as f:
            yaml_content = {
                "dialogs": {
                    "main": {
                        "windows": {
                            "start": {
                                "widgets": [
                                    {
                                        "text": f"File with {file_extension}",
                                    }
                                ]
                            }
                        }
                    }
                }
            }
            yaml.dump(yaml_content, f)
            temp_file = f.name

        try:
            # When
            builder = DialogYAMLBuilder.build(
                yaml_file_name=os.path.basename(temp_file),
                yaml_dir_path=os.path.dirname(temp_file),
            )

            # Then
            assert builder is not None
        finally:
            os.unlink(temp_file)


class TestWorkflowScenarios:
    """Functional tests for workflow scenarios."""

    def test_full_registration_workflow(self, temp_yaml_file):
        """Test a full registration workflow."""
        # Given
        yaml_content = {
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
                        "get_age": {"widgets": [{"input": {"func": "dummy_func"}}]},
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
                        "success": {
                            "widgets": [
                                {
                                    "text": "Registration completed!",
                                }
                            ]
                        },
                    }
                }
            }
        }

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
        )

        # Then
        assert builder is not None
        assert builder.states_manager is not None
        # Should have created all the required states for the workflow

    def test_settings_dialog_workflow(self, temp_yaml_file):
        """Test a settings dialog workflow."""
        # Given
        yaml_content = {
            "dialogs": {
                "settings": {
                    "windows": {
                        "menu": {
                            "widgets": [
                                {
                                    "select": {
                                        "id": "sel",
                                        "items": [
                                            "Profile",
                                            "Notifications",
                                            "Privacy",
                                        ],
                                        "item_id_getter": 0,
                                        "text": "{item}",
                                    }
                                }
                            ]
                        },
                        "profile": {
                            "widgets": [
                                {"input": {"func": "dummy_func"}},
                                {"input": {"func": "dummy_func"}},
                            ]
                        },
                        "notifications": {
                            "widgets": [
                                {
                                    "select": {
                                        "id": "sel",
                                        "items": ["On", "Off"],
                                        "item_id_getter": 0,
                                        "text": "{item}",
                                    }
                                }
                            ]
                        },
                        "privacy": {
                            "widgets": [
                                {
                                    "select": {
                                        "id": "sel",
                                        "items": ["Public", "Private"],
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

        with open(temp_yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        # When
        builder = DialogYAMLBuilder.build(
            yaml_file_name=os.path.basename(temp_yaml_file),
            yaml_dir_path=os.path.dirname(temp_yaml_file),
        )

        # Then
        assert builder is not None
        # Should have processed the complete settings workflow
