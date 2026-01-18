"""Unit tests for YAMLModelFactory component."""

import pytest
from aiogram_dialog.api.internal import Widget

from dialog_yml.exceptions import (
    ModelRegistrationError,
    InvalidTagName,
    DialogYamlException,
)
from dialog_yml.models import YAMLModelFactory, YAMLModel


class YAMLSubModel(YAMLModel):
    def to_object(self):
        from unittest.mock import Mock

        return Mock(spec=Widget)

    key1: str = ""
    key2: str = ""

    @classmethod
    def to_model(cls, data):
        return cls(**data)


class NotYAMLModel:
    key1: str
    key2: str

    def __init__(self, key1: str, key2: str = "None"):
        self.key1 = key1
        self.key2 = key2


class TestYAMLModelFactory:
    """Unit tests for YAMLModelFactory functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixture to reset model classes before each test."""
        YAMLModelFactory._models_classes = {}

    def test_get_model_class_retrieve_registered(self):
        """Test retrieving a registered model class."""
        # Given
        tag = "tag"
        model_class = YAMLModel
        YAMLModelFactory._models_classes = {tag: model_class}

        # When
        result = YAMLModelFactory.get_model_class(tag)

        # Then
        assert result == model_class

    def test_get_model_class_return_none_if_not_found(self):
        """Test returning None if tag not found."""
        # Given
        tag = "nonexistent"

        # When
        result = YAMLModelFactory.get_model_class(tag)

        # Then
        assert result is None

    @pytest.mark.parametrize(
        "tag,model_class",
        [
            ("valid_tag", YAMLModel),
            ("valid_tag_with_underscore", YAMLModel),
            ("valid-tag-with-hyphen", YAMLModel),
            ("valid_tag_with_digits_123", YAMLModel),
            ("validtagwithletters", YAMLModel),
        ],
    )
    def test_is_valid_returns_true_for_valid_combinations(self, tag, model_class):
        """Test that valid tag and model combinations return True."""
        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    @pytest.mark.parametrize(
        "tag,model_class,expected_exception",
        [
            ("", YAMLModel, InvalidTagName),
            (123, YAMLModel, InvalidTagName),
            ("123", YAMLModel, InvalidTagName),
            ("tag_with_special_characters!", YAMLModel, InvalidTagName),
        ],
    )
    def test_is_valid_raises_for_invalid_combinations(
        self, tag, model_class, expected_exception
    ):
        """Test that invalid tag and model combinations raise exceptions."""
        # When, Then
        with pytest.raises(expected_exception):
            YAMLModelFactory._is_valid(tag, model_class)

    @pytest.mark.parametrize(
        "models_classes,expected_success",
        [
            (
                {
                    "tag1": YAMLModel,
                    "tag2": YAMLSubModel,
                    "tag3": YAMLSubModel,
                },
                True,
            ),
            ({}, True),  # Empty dict should work
        ],
    )
    def test_set_valid_dictionary_of_model_classes(self, models_classes, expected_success):
        """Test setting a valid dictionary of model classes."""
        # When
        YAMLModelFactory.set_classes(models_classes)

        # Then
        assert YAMLModelFactory._models_classes == models_classes

    @pytest.mark.parametrize(
        "models_classes,expected_exception",
        [
            ({123: YAMLModelFactory}, DialogYamlException),  # Non-string key
            (
                {"tag1": NotYAMLModel},
                DialogYamlException,
            ),  # Non-YAMLModel value
            ({"123": YAMLModelFactory}, InvalidTagName),  # Key with only digits
            (
                {"tag!": YAMLModelFactory},
                InvalidTagName,
            ),  # Key with special chars
            ("not a dictionary", DialogYamlException),  # Not a dictionary
            (None, DialogYamlException),  # None value
        ],
    )
    def test_set_dictionary_raises_for_invalid_inputs(
        self, models_classes, expected_exception
    ):
        """Test that setting invalid dictionaries raises exceptions."""
        # When/Then
        with pytest.raises(expected_exception):
            YAMLModelFactory.set_classes(models_classes)

    @pytest.mark.parametrize(
        "tag,model_class,expected_success",
        [
            ("tag1", YAMLModel, True),
            ("tag2", YAMLSubModel, True),
        ],
    )
    def test_register_custom_model_class_with_unique_tag(
        self, tag, model_class, expected_success
    ):
        """Test registering a custom model class with a unique tag."""
        # When
        YAMLModelFactory.add_model_class(tag, model_class)

        # Then
        assert YAMLModelFactory.get_model_class(tag) == model_class

    @pytest.mark.parametrize(
        "existing_tag,new_model_class,expected_exception",
        [
            (
                "Tag1",
                YAMLSubModel,
                ModelRegistrationError,
            ),  # Already registered tag
        ],
    )
    def test_register_custom_model_class_with_already_registered_tag(
        self, existing_tag, new_model_class, expected_exception
    ):
        """Test registering a model class with an already registered tag."""
        # Given
        model_class1 = YAMLModel
        YAMLModelFactory.add_model_class(existing_tag, model_class1)

        # When, Then
        with pytest.raises(expected_exception):
            YAMLModelFactory.add_model_class(existing_tag, new_model_class)

    @pytest.mark.parametrize(
        "invalid_tag,expected_exception",
        [
            ("!@#$%^&*()", InvalidTagName),
            ("", InvalidTagName),
            (123, InvalidTagName),
            (None, InvalidTagName),
        ],
    )
    def test_register_custom_model_class_with_invalid_tag(
        self, invalid_tag, expected_exception
    ):
        """Test registering a model class with an invalid tag."""
        # Given
        model_class = YAMLModel

        # When/Then
        with pytest.raises(expected_exception):
            YAMLModelFactory.add_model_class(invalid_tag, model_class)

    def test_multiple_model_registration(self):
        """Test registering multiple model classes."""
        # Given
        tag1, tag2, tag3 = "tag1", "tag2", "tag3"
        model_class1, model_class2, model_class3 = (
            YAMLModel,
            YAMLSubModel,
            YAMLSubModel,
        )

        # When
        YAMLModelFactory.add_model_class(tag1, model_class1)
        YAMLModelFactory.add_model_class(tag2, model_class2)
        YAMLModelFactory.add_model_class(tag3, model_class3)

        # Then
        assert YAMLModelFactory.get_model_class(tag1) == model_class1
        assert YAMLModelFactory.get_model_class(tag2) == model_class2
        assert YAMLModelFactory.get_model_class(tag3) == model_class3

    def test_create_model_success(self):
        """Test successful model creation."""
        # Given
        data = {"test": {"key1": "value1", "key2": "value2"}}
        YAMLModelFactory.set_classes({"test": YAMLSubModel})

        # When
        result = YAMLModelFactory.create_model(data)

        # Then
        assert isinstance(result, YAMLSubModel)
        assert result.key1 == data["test"]["key1"]
        assert result.key2 == data["test"]["key2"]

    def test_create_model_success_with_optional_field(self):
        """Test successful model creation with missing optional field."""
        # Given
        data = {"test": {"key1": "value1"}}  # Missing optional field
        YAMLModelFactory.set_classes({"test": YAMLSubModel})

        # When
        result = YAMLModelFactory.create_model(data)

        # Then
        assert isinstance(result, YAMLSubModel)
        assert result.key1 == data["test"]["key1"]

    @pytest.mark.parametrize(
        "invalid_data,expected_exception",
        [
            ("not dictionary", DialogYamlException),  # Wrong data type
        ],
    )
    def test_create_model_raises_for_invalid_data(self, invalid_data, expected_exception):
        """Test that creating a model with invalid data raises exceptions."""
        # Given
        YAMLModelFactory.set_classes({"test": YAMLSubModel})

        # When/Then
        with pytest.raises(expected_exception):
            YAMLModelFactory.create_model(invalid_data)
