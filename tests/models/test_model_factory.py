from typing import Self

import pytest
from aiogram_dialog.api.internal import Widget
from pydantic import ValidationError

from dialog_yml.exceptions import (
    ModelRegistrationError,
    InvalidTagName,
    DialogYamlException,
)
from dialog_yml.models import YAMLModelFactory, YAMLModel


class YAMLSubModel(YAMLModel):
    def to_object(self) -> Widget:
        pass

    key1: str
    key2: str | None = None

    @classmethod
    def to_model(cls, data: dict) -> Self:
        return YAMLSubModel(**data)


class NotYAMLModel:
    key1: str
    key2: str

    def __init__(self, key1: str, key2: str = "None"):
        self.key1 = key1
        self.key2 = key2


class TestYAMLModelClass:
    @pytest.fixture(autouse=True)
    def setup(self):
        YAMLModelFactory._models_classes = {}


class TestIsValidModelClass(TestYAMLModelClass):
    def test_valid_tag_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag"
        model_class = YAMLModel

        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_underscore_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag_with_underscore"
        model_class = YAMLModel

        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_hyphen_and_model_class_returns_true(self):
        # Given
        tag = "valid-tag-with-hyphen"
        model_class = YAMLModel

        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_digits_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag_with_digits_123"
        model_class = YAMLModel

        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_letters_and_model_class_returns_true(self):
        # Given
        tag = "validtagwithletters"
        model_class = YAMLModel

        # When
        result = YAMLModelFactory._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_empty_tag_raises_invalid_tag_name(self):
        # Given
        tag = ""
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory._is_valid(tag, model_class)

    def test_non_string_tag_raises_invalid_tag_name(self):
        # Given
        tag = 123
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory._is_valid(tag, model_class)

    def test_tag_with_only_digits_raises_invalid_tag_name(self):
        # Given
        tag = "123"
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory._is_valid(tag, model_class)

    def test_tag_with_special_characters_raises_invalid_tag_name(self):
        # Given
        tag = "tag_with_special_characters!"
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory._is_valid(tag, model_class)


class TestSetModelClasses(TestYAMLModelClass):
    def test_set_valid_dictionary_of_model_classes(self):
        # Given
        models_classes = {
            "tag1": YAMLModel,
            "tag2": YAMLSubModel,
            "tag3": YAMLSubModel,
        }

        # When
        YAMLModelFactory.set_classes(models_classes)

        # Then
        assert YAMLModelFactory._models_classes == models_classes

    def test_set_empty_dictionary_of_model_classes(self):
        # Given
        models_classes = {}

        # When
        YAMLModelFactory.set_classes(models_classes)

        # Then
        assert YAMLModelFactory._models_classes == models_classes

    def test_set_dictionary_with_non_string_key(self):
        # Given
        models_classes = {123: YAMLModelFactory}

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.set_classes(models_classes)

    def test_set_dictionary_with_non_yamlmodel_value(self):
        # Given
        models_classes = {"tag1": NotYAMLModel}

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.set_classes(models_classes)

    def test_set_dictionary_with_key_only_digits(self):
        # Given
        models_classes = {"123": YAMLModelFactory}

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.set_classes(models_classes)

    def test_set_dictionary_with_key_special_characters(self):
        # Given
        models_classes = {"tag!": YAMLModelFactory}

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.set_classes(models_classes)

    def test_raise_dialog_yml_exception_when_models_classes_not_dictionary(
        self,
    ):
        # Given
        models_classes = "not a dictionary"

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.set_classes(models_classes)

    def test_raise_dialog_yml_exception_when_models_classes_not_dictionary_of_strings_to_yamlmodel_classes(
        self,
    ):
        # Given
        models_classes = {"tag1": YAMLModelFactory, "tag2": "NotYAMLModel"}

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.set_classes(models_classes)

    def test_raise_dialog_yml_exception_when_models_classes_is_none(self):
        # Given
        models_classes = None

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.set_classes(models_classes)


class TestRegisterModelClass(TestYAMLModelClass):
    def test_register_custom_model_class_with_unique_tag(self):
        # Given
        tag = "tag1"
        model_class1 = YAMLModel

        # When
        YAMLModelFactory.add_model_class(tag, model_class1)

        # Then
        assert YAMLModelFactory.get_model_class(tag) == model_class1

    def test_register_multiple_custom_model_classes_with_unique_tags(self):
        # Given
        tag1 = "tag1"
        tag2 = "tag2"
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModelFactory.add_model_class(tag1, model_class1)
        YAMLModelFactory.add_model_class(tag2, model_class2)

        # Then
        assert YAMLModelFactory.get_model_class(tag1) == model_class1
        assert YAMLModelFactory.get_model_class(tag2) == model_class2

    def test_register_custom_model_class_with_previously_registered_tag_and_different_class(
        self,
    ):
        # Given
        tag = "tag1"  # Use a different tag
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModelFactory.add_model_class(tag, model_class1)

        # Then
        with pytest.raises(ModelRegistrationError):
            YAMLModelFactory.add_model_class(tag, model_class2)

    def test_register_custom_model_class_with_tag_containing_special_characters(
        self,
    ):
        # Given
        tag = "!@#$%^&*()"
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_empty_tag(self):
        # Given
        tag = ""
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_non_string_tag(self):
        # Given
        tag = 123
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_already_registered_tag(self):
        # Given
        tag = "Tag1"
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModelFactory.add_model_class(tag, model_class1)

        # Then
        with pytest.raises(ModelRegistrationError):
            YAMLModelFactory.add_model_class(tag, model_class2)

    def test_register_custom_model_class_with_none_tag(self):
        # Given
        tag = None
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModelFactory.add_model_class(tag, model_class)


class TestGetModelClass(TestYAMLModelClass):
    def test_retrieve_registered_model_class(self):
        # Given
        tag = "tag"
        model_class = YAMLModel
        YAMLModelFactory._models_classes = {tag: model_class}

        # When
        result = YAMLModelFactory.get_model_class(tag)

        # Then
        assert result == model_class

    def test_return_none_if_tag_not_found(self):
        # Given
        tag = "tag"

        # When
        result = YAMLModelFactory.get_model_class(tag)

        # Then
        assert result is None


class TestFromDataModelClass(TestYAMLModelClass):
    @pytest.fixture(autouse=True)
    def setup(self):
        tag = "test"
        YAMLModelFactory.set_classes({tag: YAMLSubModel})

    def test_to_model(self):
        # Given
        data = {"test": {"key1": "value1", "key2": "value2"}}

        # When
        result = YAMLModelFactory.create_model(data)

        # Then
        assert isinstance(result, YAMLSubModel)
        assert result.key1 == "value1"
        assert result.key2 == "value2"

    def test_raise_exception_when_model_is_invalid(self):
        # Given
        data = {"test": {"key1": 123, "key2": [1, "2", 0.3]}}

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.create_model(data)

    def test_raise_exception_when_not_correct_model_data(self):
        # Given
        model_class = YAMLSubModel
        data = {"key1": 123, "key2": [1, "2", 0.3]}

        # When/Then
        with pytest.raises(ValidationError):
            model_class.to_model(data)

    def test_to_model_with_missing_key(self):
        # Given
        data = {
            "test": {
                "key1": "value1",
            }
        }

        # When
        result = YAMLModelFactory.create_model(data)

        # Then
        assert isinstance(result, YAMLSubModel)
        assert result.key1 == "value1"
        assert result.key2 is None

    def test_yaml_model_setup(setup):
        # Given
        tag = "test"

        # When
        result = YAMLModelFactory.get_model_class(tag)

        # Then
        assert result == YAMLSubModel

    def test_from_data_with_not_correct_data_type(self):
        # Given
        data = "not dictionary"

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModelFactory.create_model(data)
