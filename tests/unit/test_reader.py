"""Unit tests for YAMLReader component."""

import pytest
from unittest.mock import mock_open, patch
import yaml

from dialog_yml.reader import YAMLReader


class TestYAMLReader:
    """Unit tests for YAMLReader functionality."""

    def test_file_not_found(self):
        """Test reading non-existent file raises FileNotFoundError."""
        # Given
        data_file_path = "file_not_found.yaml"
        data_dir_path = "/path/to/directory"

        with patch("os.path.exists", return_value=False):
            # When/Then
            with pytest.raises(FileNotFoundError):
                YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

    def test_valid_yaml_file(self):
        """Test reading valid YAML file."""
        # Given
        data_file_path = "valid.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"key": "value"}

        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="key: value")):
                # When
                result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

        # Then
        assert result == expected_data

    @pytest.mark.parametrize(
        "yaml_content,expected_result",
        [
            ("{}", {}),
            ("key: value", {"key": "value"}),
            ("list:\n  - item1\n  - item2", {"list": ["item1", "item2"]}),
            (
                "nested:\n  key:\n    deep: value",
                {"nested": {"key": {"deep": "value"}}},
            ),
        ],
    )
    def test_various_yaml_contents(self, yaml_content, expected_result):
        """Test reading various YAML content structures."""
        # Given
        data_file_path = "test.yaml"
        data_dir_path = "/path/to/directory"

        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                # When
                result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

        # Then
        assert result == expected_result

    def test_corrupted_yaml_syntax(self):
        """Test that corrupted YAML raises YAMLError."""
        # Given
        data_file_path = "corrupted.yaml"
        data_dir_path = "/path/to/directory"

        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="key: value\ninvalid")):
                # When/Then
                with pytest.raises(yaml.YAMLError):
                    YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

    @pytest.mark.parametrize("file_extension", [".yaml", ".yml", ""])
    def test_file_extension_handling(self, file_extension):
        """Test handling of different file extensions."""
        # Given
        data_file_path = f"test{file_extension}"
        data_dir_path = "/path/to/directory"
        expected_data = {"key": "value"}

        def mock_exists(path):
            if file_extension:
                return path.endswith(f"test{file_extension}")
            else:
                # Simulate fallback behavior when no extension provided
                return path.endswith(("test.yaml", "test.yml"))

        with patch("os.path.exists", side_effect=mock_exists):
            with patch("builtins.open", mock_open(read_data="key: value")):
                # When
                result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

        # Then
        assert result == expected_data
