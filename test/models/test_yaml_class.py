import pytest
from pydantic import BaseModel

from core.exceptions import ModelRegistrationError, InvalidTagName, DialogYamlException
from core.models import YAMLModel


class YAMLSubModel(YAMLModel):
    pass


class NotYAMLModel:
    pass


class TestYAMLModelClass:
    @pytest.fixture(autouse=True)
    def setup(self):
        YAMLModel._models_classes = {}


class TestIsValidModelClass(TestYAMLModelClass):
    def test_valid_tag_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag"
        model_class = YAMLModel

        # When
        result = YAMLModel._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_underscore_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag_with_underscore"
        model_class = YAMLModel

        # When
        result = YAMLModel._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_hyphen_and_model_class_returns_true(self):
        # Given
        tag = "valid-tag-with-hyphen"
        model_class = YAMLModel

        # When
        result = YAMLModel._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_digits_and_model_class_returns_true(self):
        # Given
        tag = "valid_tag_with_digits_123"
        model_class = YAMLModel

        # When
        result = YAMLModel._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_valid_tag_with_letters_and_model_class_returns_true(self):
        # Given
        tag = "validtagwithletters"
        model_class = YAMLModel

        # When
        result = YAMLModel._is_valid(tag, model_class)

        # Then
        assert result is True

    def test_empty_tag_raises_invalid_tag_name(self):
        # Given
        tag = ""
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModel._is_valid(tag, model_class)

    def test_non_string_tag_raises_invalid_tag_name(self):
        # Given
        tag = 123
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModel._is_valid(tag, model_class)

    def test_tag_with_only_digits_raises_invalid_tag_name(self):
        # Given
        tag = "123"
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModel._is_valid(tag, model_class)

    def test_tag_with_special_characters_raises_invalid_tag_name(self):
        # Given
        tag = "tag_with_special_characters!"
        model_class = YAMLModel

        # When, Then
        with pytest.raises(InvalidTagName):
            YAMLModel._is_valid(tag, model_class)


class TestSetModelClasses(TestYAMLModelClass):
    def test_set_valid_dictionary_of_model_classes(self):
        # Given
        models_classes = {
            'tag1': YAMLModel,
            'tag2': YAMLSubModel,
            'tag3': YAMLSubModel
        }

        # When
        YAMLModel.set_classes(models_classes)

        # Then
        assert YAMLModel._models_classes == models_classes

    def test_set_empty_dictionary_of_model_classes(self):
        # Given
        models_classes = {}

        # When
        YAMLModel.set_classes(models_classes)

        # Then
        assert YAMLModel._models_classes == models_classes

    def test_set_dictionary_with_non_string_key(self):
        # Given
        models_classes = {
            123: YAMLModel
        }

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModel.set_classes(models_classes)

    def test_set_dictionary_with_non_yamlmodel_value(self):
        # Given
        models_classes = {
            'tag1': NotYAMLModel
        }

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModel.set_classes(models_classes)

    def test_set_dictionary_with_key_only_digits(self):
        # Given
        models_classes = {
            '123': YAMLModel
        }

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.set_classes(models_classes)

    def test_set_dictionary_with_key_special_characters(self):
        # Given
        models_classes = {
            'tag!': YAMLModel
        }

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.set_classes(models_classes)

    def test_raise_dialog_yaml_exception_when_models_classes_not_dictionary(self):
        # Given
        models_classes = 'not a dictionary'

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModel.set_classes(models_classes)

    def test_raise_dialog_yaml_exception_when_models_classes_not_dictionary_of_strings_to_yamlmodel_classes(self):
        # Given
        models_classes = {
            'tag1': YAMLModel,
            'tag2': 'NotYAMLModel'
        }

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModel.set_classes(models_classes)

    def test_raise_dialog_yaml_exception_when_models_classes_is_none(self):
        # Given
        models_classes = None

        # When/Then
        with pytest.raises(DialogYamlException):
            YAMLModel.set_classes(models_classes)


class TestRegisterModelClass(TestYAMLModelClass):

    def test_register_custom_model_class_with_unique_tag(self):
        # Given
        tag = "tag1"
        model_class1 = YAMLModel

        # When
        YAMLModel.add_model_class(tag, model_class1)

        # Then
        assert YAMLModel.get_model_class(tag) == model_class1

    def test_register_multiple_custom_model_classes_with_unique_tags(self):
        # Given
        tag1 = "tag1"
        tag2 = "tag2"
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModel.add_model_class(tag1, model_class1)
        YAMLModel.add_model_class(tag2, model_class2)

        # Then
        assert YAMLModel.get_model_class(tag1) == model_class1
        assert YAMLModel.get_model_class(tag2) == model_class2

    def test_register_custom_model_class_with_previously_registered_tag_and_different_class(self):
        # Given
        tag = "tag1"  # Use a different tag
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModel.add_model_class(tag, model_class1)

        # Then
        with pytest.raises(ModelRegistrationError):
            YAMLModel.add_model_class(tag, model_class2)

    def test_register_custom_model_class_with_tag_containing_special_characters(self):
        # Given
        tag = "!@#$%^&*()"
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_empty_tag(self):
        # Given
        tag = ""
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_non_string_tag(self):
        # Given
        tag = 123
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.add_model_class(tag, model_class)

    def test_register_custom_model_class_not_subclass_of_YAMLModel(self):
        # TODO: fix this test

        # Given
        tag = "tag1"
        model_class = BaseModel

        # When/Then
        with pytest.raises(ModelRegistrationError):
            YAMLModel.add_model_class(tag, model_class)

    def test_register_custom_model_class_with_already_registered_tag(self):
        # Given
        tag = "Tag1"
        model_class1 = YAMLModel
        model_class2 = YAMLSubModel

        # When
        YAMLModel.add_model_class(tag, model_class1)

        # Then
        with pytest.raises(ModelRegistrationError):
            YAMLModel.add_model_class(tag, model_class2)

    def test_register_custom_model_class_with_none_tag(self):
        # Given
        tag = None
        model_class = YAMLModel

        # When/Then
        with pytest.raises(InvalidTagName):
            YAMLModel.add_model_class(tag, model_class)


class TestGetModelClass(TestYAMLModelClass):
    def test_retrieve_registered_model_class(self):
        # Given
        tag = 'tag'
        model_class = YAMLModel
        YAMLModel._models_classes = {tag: model_class}

        # When
        result = YAMLModel.get_model_class(tag)

        # Then
        assert result == model_class

    def test_return_none_if_tag_not_found(self):
        # Given
        tag = 'tag'

        # When
        result = YAMLModel.get_model_class(tag)

        # Then
        assert result is None


class TestFromDataModelClass(TestYAMLModelClass):

    @pytest.fixture(autouse=True)
    def setup(self):
        YAMLModel.set_classes({
            'tag': YAMLSubModel,
            'tag1': YAMLSubModel,
            'tag2': YAMLSubModel,
        })

    # TODO: create tests
