import pytest
import yaml

from src.reader import YAMLReader


class TestYAMLReader:
    def test_file_not_found(self, mocker):
        # Given
        data_file_path = "file_not_found.yaml"
        data_dir_path = "/path/to/directory"
        mocker.patch("os.path.exists", return_value=False)

        # When/Then
        with pytest.raises(FileNotFoundError):
            YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

    def test_valid_yaml_file(self, mocker):
        # Given
        data_file_path = "valid.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"key": "value"}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="key: value"))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_empty_dictionary(self, mocker):
        # Given
        data_file_path = "empty.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="{}"))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_nested_dictionaries(self, mocker):
        # Given
        data_file_path = "nested.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"key1": {"key2": "value"}}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="key1:\n  key2: value"))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_list(self, mocker):
        # Given
        data_file_path = "list.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = ["item1", "item2", "item3"]
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data="- item1\n- item2\n- item3"),
        )
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_null_value(self, mocker):
        # Given
        data_file_path = "null.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = None
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="null"))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_non_existent_key(self, mocker):
        # Given
        data_file_path = "non_existent_key.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = None
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="key: value"))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result.get("other_key") == expected_data

    def test_corrupted_yaml_syntax(self, mocker):
        # Given
        data_file_path = "corrupted.yaml"
        data_dir_path = "/path/to/directory"
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="key: value\ninvalid"))
        # When/Then
        with pytest.raises(yaml.YAMLError):
            YAMLReader.read_data_to_dict(data_file_path, data_dir_path)

    def test_large_dictionary(self, mocker):
        # Given
        data_file_path = "large.yaml"
        data_dir_path = "/path/to/directory"
        size = 10000
        expected_data = {str(i): i for i in range(size)}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data="\n".join(f'"{i}": {i}' for i in range(size))),
        )
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_special_characters(self, mocker):
        # Given
        data_file_path = "special_characters.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"key": "!@#$%^&*()"}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data='key: "!@#$%^&*()"'))
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_integers_floats_strings(self, mocker):
        # Given
        data_file_path = "int_float_str.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"int": 1, "float": 1.5, "str": "value"}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data="int: 1\nfloat: 1.5\nstr: value"),
        )
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data

    def test_boolean_values(self, mocker):
        # Given
        data_file_path = "boolean.yaml"
        data_dir_path = "/path/to/directory"
        expected_data = {"true": True, "false": False}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data='"true": true\n"false": false'),
        )
        # When
        result = YAMLReader.read_data_to_dict(data_file_path, data_dir_path)
        # Then
        assert result == expected_data
