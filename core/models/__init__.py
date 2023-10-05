"""The `core.models` module provides the YAMLModel class for creating YAML models.

YAMLModel is a subclass of Pydantic BaseModel and offers functionality for working with YAML data
and creating instances of custom model classes based on the YAML data.

Features:
-----------
- Allows the registration of custom model classes with unique tags.
- Provides a method to create instances of custom model classes from YAML data.
- Supports the retrieval of the registered model class based on the tag.

Classes:
-----------
- YAMLModel: Static class for creating YAML models.
"""

import logging
import re
from typing import Type, Union, Dict, Any

from pydantic import BaseModel, ValidationError

from core.exceptions import ModelRegistrationError, InvalidTagName, DialogYamlException

logger = logging.getLogger(__name__)


class YAMLModel(BaseModel):
    """Static class for creating YAML models.

    The `YAMLModel` class is a subclass of `BaseModel` from the Pydantic library.
    It provides functionality for working with YAML data and creating instances
    of custom model classes based on the YAML data.

    - Allows the registration of custom model classes with unique tags.
    - Provides a method to create instances of custom model classes from YAML data.
    - Supports the retrieval of the registered model class based on the tag.

    :ivar _models_classes: A dictionary that maps tag to model class.
    :vartype _models_classes: Dict[str, Type['YAMLModel']]
    """

    _models_classes: Dict[str, Type['YAMLModel']] = {}

    @classmethod
    def is_valid_tag(cls, tag: str) -> bool:
        if not tag or not isinstance(tag, str):
            raise InvalidTagName(tag, '{tag!r} must be non-empty string')

        if tag.isdigit():
            raise InvalidTagName(tag, '{tag!r} must contain a letters, not only numbers')

        if not re.fullmatch(r'[a-zA-Z0-9_-]+', tag):
            raise InvalidTagName(tag, '{tag!r} must contains only latin letters and numbers')

        return True

    @classmethod
    def is_valid_model_class(cls, tag: str, model_class: Type['YAMLModel']) -> bool:
        if not isinstance(model_class, YAMLModel.__class__):
            raise ModelRegistrationError(
                tag, model_class,
                message='{model_class!r} must be type of YAMLModel'
            )

        return True

    @classmethod
    def _is_valid(cls, tag: str, model_class: Type['YAMLModel']) -> bool:
        cls.is_valid_tag(tag)
        cls.is_valid_model_class(tag, model_class)
        return True

    @classmethod
    def add_model_class(cls, tag: str, model_class: Type['YAMLModel']):
        """Registers a custom model class with a unique tag.

        :param tag: A unique tag for the custom model class.
        :type tag: Str
        :param model_class: The custom model class to be registered.
        :type model_class: Type['YAMLModel']

        :raises ModelRegistrationError: When a model with the same tag has already been registered.
        """

        if cls._is_valid(tag, model_class):

            if registered_model_class := cls.get_model_class(tag):
                raise ModelRegistrationError(
                    tag, registered_model_class,
                    message='{tag!r} already registered with {model_class!r}'
                )

            cls._models_classes[tag] = model_class

    @classmethod
    def get_model_class(cls, tag: str) -> Union[Type['YAMLModel'], None]:
        """Retrieves a registered custom model class based on its tag.

        :param tag: The tag of the custom model class to retrieve.
        :type tag: Str

        :return: The custom model class associated with the given tag or None if not found.
        :rtype: Type['YAMLModel'] or None
        """
        logger.debug(f'Get class for tag {tag!r}')
        return cls._models_classes.get(tag)

    @classmethod
    def set_classes(cls, models_classes: Dict[str, Type['YAMLModel']]) -> None:
        """Sets the registered custom model classes.

        :param models_classes: A dictionary of custom model classes with their tags.
        :type models_classes: Dict[str, Type['YAMLModel']]

        :raises DialogYamlException: When `models_classes` is not a valid dictionary of model classes.
        """
        if not isinstance(models_classes, dict):
            raise DialogYamlException("models_classes must be a dictionary of strings to YAMLModel classes")

        for key, value in models_classes.items():
            cls._is_valid(key, value)

        cls._models_classes = models_classes

    @classmethod
    def from_data(cls, yaml_data: Dict[str, Any]) -> 'YAMLModel':
        """Creates an instance of a custom model class based on YAML data.

        The `from_data` method in the `YAMLModel` class is used to create an instance
        of a custom model class based on YAML data.

        It retrieves the model class based on the tag provided in the YAML data
        and then creates an instance of that class using the data associated with the tag.

        :param yaml_data: A dictionary representing the YAML data.
            The keys in the dictionary are the tags, and the
            values are the associated data for each tag.
        :type yaml_data: Dict[str, Any]

        :return: An instance of the custom model class based on the existing class
            in the `cls._models_classes`, founded by `tag` in `yaml_data`.
        :rtype: YAMLModel

        :raises DialogYamlException: When `yaml_data` is `None` or an empty dictionary.
        :raises InvalidTagName: When a tag key does not exist in the `cls._models_classes`.
        """
        if not yaml_data or not isinstance(yaml_data, dict):
            raise DialogYamlException("yaml_data must be a non-empty dictionary")

        tag = next(iter(yaml_data))  # getting first key
        cls.is_valid_tag(tag)
        model_class = cls.get_model_class(tag)
        data = yaml_data[tag]
        logger.debug(f'Parse tag {tag!r}: {data}')
        try:
            model = model_class.to_model(data)
        except ValidationError as e:
            raise DialogYamlException(
                f'Failed to parse tag {tag!r}: {e}'
            )
        return model
