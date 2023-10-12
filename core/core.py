import logging
import os
from typing import Type, List, Dict, Any, Self

from aiogram import Router
from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Dialog, setup_dialogs
from pydantic import BaseModel

from .exceptions import DialogYamlException, InvalidTagName, InvalidTagDataType
from .middleware import DialogYAMLMiddleware
from .reader import YAMLReader
from .states import YAMLStatesManager
from .models import YAMLModelFactory
from .models.base import YAMLModel
from .models.window import WindowModel
from .models.dialog import DialogModel
from .models.widgets import widget_classes
from .models.funcs import FuncsRegistry, func_classes

logger = logging.getLogger(__name__)

models_classes = dict(
    window=WindowModel, dialog=DialogModel, **func_classes, **widget_classes
)


class DialogYAMLBuilder:
    funcs_registry: FuncsRegistry
    states_manager: YAMLStatesManager
    _router: Router
    _dialogs: List[Dialog] = []

    def __init__(
        self, yaml_file_name: str, yaml_dir_path: str = None, router: Router = Router()
    ):
        logger.debug("Initialize DialogYAMLBuilder")

        self.yaml_file_name = yaml_file_name
        self.yaml_dir_path = yaml_dir_path
        self._router = router

        self.funcs_registry = FuncsRegistry()
        self.states_manager = YAMLStatesManager()
        self.model_factory = YAMLModelFactory
        self.model_factory.set_classes(models_classes)

    @property
    def router(self) -> Router:
        return self._router

    @classmethod
    def build(
        cls,
        yaml_file_name: str,
        yaml_dir_path: str = None,
        states: List[Type[StatesGroup]] = None,
        models: Dict[str, Type[YAMLModel]] = None,
        router: Router = Router(),
    ) -> Self:
        """Builds the DialogYAMLBuilder and initializes the aiogram dialogs router.

        :param yaml_file_name: The name of the YAML file.
        :type yaml_file_name: str
        :param yaml_dir_path: The path to the directory containing the YAML file.
        :type yaml_dir_path: str (optional, default: None)
        :param states: The states to be included in the router.
        :type states: List[Type[StatesGroup]] (optional, default: None)
        :param models: The custom models to be included in the router.
        :type models: Dict[str, Type[YAMLModel]] (optional, default: None)
        :param router: The router to be used.
        :type router: Router (optional, default: Router())

        :return: The router.
        :rtype: Router
        """

        logger.debug(
            f"Build {yaml_file_name!r} with states {states!r} and models {models!r}"
        )
        dialog_builder = DialogYAMLBuilder(yaml_file_name, yaml_dir_path)
        dialog_builder.register_custom_models(models)
        dialog_builder.register_custom_states(states)

        dialogs = dialog_builder._build(yaml_file_name, yaml_dir_path)
        dialog_builder._dialogs = dialogs
        router.include_routers(*dialogs)

        router.message.middleware.register(
            DialogYAMLMiddleware(dialog_yaml=dialog_builder)
        )
        router.callback_query.middleware.register(
            DialogYAMLMiddleware(dialog_yaml=dialog_builder)
        )
        router.errors.middleware.register(
            DialogYAMLMiddleware(dialog_yaml=dialog_builder)
        )
        dialog_builder._router = router

        setup_dialogs(router)
        return dialog_builder

    def register_custom_models(
        self, custom_models: Dict[str, Type[YAMLModel]], replace_existing: bool = False
    ) -> None:
        """Registers custom models.

        :param custom_models: The custom models.
        :type custom_models: Dict[str, Type[YAMLModel]]
        :param replace_existing: Whether to replace existing models.
        :type replace_existing: bool (optional, default: False)

        :return: None
        :rtype: None
        """

        if not custom_models:
            return

        for yaml_tag, custom_model in custom_models.items():
            logger.debug(
                f"Register tag {yaml_tag!r} for model {custom_model.__name__!r}"
            )
            self.model_factory.add_model_class(yaml_tag, custom_model, replace_existing)

    def register_custom_states(self, custom_states: List[Type[StatesGroup]]) -> None:
        """Registers custom states.

        :param custom_states: The custom states.
        :type custom_states: List[Type[StatesGroup]]

        :return: None
        :rtype: None
        """

        if not custom_states:
            return

        for custom_state in custom_states:
            self.states_manager.include_states_group_by_class(custom_state)

    def _build(self, file_name: str, dir_path: str = None) -> List[Dialog]:
        """Builds the Dialog instance from the YAML file.

        :param file_name: The name of the YAML file.
        :type file_name: str
        :param dir_path: The path to the directory containing the YAML file.
        :type dir_path: str (optional, default: None)

        :return: The dialogs.
        :rtype: List[Dialog]
        """

        logger.debug("Build dialogs")
        data = YAMLReader.read_data_to_dict(
            data_file_path=file_name, data_dir_path=dir_path
        )
        data_file_path = os.path.join(dir_path, file_name)

        if not data:
            raise DialogYamlException(
                f"YAML data file {data_file_path!r} not provided!"
            )

        self.check_yaml_data_base_structure(data)
        self.states_manager.build_states_from_yaml_data(data)

        dialog_models = {}
        for group_name, dialog_model_data in data["dialogs"].items():
            logger.debug(f"Build dialog data {group_name!r}")
            dialog_model_data["windows"] = self._build_windows(
                group_name, dialog_model_data["windows"]
            )
            dialog_model = DialogModel.to_model(dialog_model_data)
            dialog_models[group_name] = dialog_model

        dialogs = self._build_dialogs(dialog_models)

        return dialogs

    def _build_dialogs(self, dialog_models: Dict) -> List[Dialog]:
        logger.debug("Create dialogs")
        dialogs = [dialog_model.to_object() for dialog_model in dialog_models.values()]

        return dialogs

    def _build_windows(self, group_name, windows_data):
        windows = [
            self._build_window(group_name, state_name, window_data)
            for state_name, window_data in windows_data.items()
        ]

        return windows

    def _build_window(
        self, group_name: str, state_name: str, window_data: Dict
    ) -> BaseModel:
        logger.debug(f"Build window data {state_name!r}")
        window_data["state"] = self.states_manager.format_state_name(
            group_name, state_name
        )
        window_data["widgets"] = self._build_widgets(window_data["widgets"])
        window_model = self.model_factory.create_model({"window": window_data})

        return window_model

    def _build_widgets(self, widgets_data: List[dict]):
        return [self._build_widget(widget_data) for widget_data in widgets_data]

    def _build_widget(self, widget_data: Dict):
        widget = self.model_factory.create_model(widget_data)
        return widget

    @classmethod
    def check_yaml_data_base_structure(cls, input_data: Dict[str, Dict]) -> bool:
        """Check provided input data for valid dialog-yaml structure.

        Tags "dialogs", "windows", "widgets" are !required.

        Example valid data:
            input_data = {
                'dialogs': {
                    'group_name': {
                        'windows': {
                            'state_name': {
                                'widgets': [], **window_kwargs
                            },
                            'other_state_name': {'widgets': [], ...}
                        },
                        **dialog_kwargs
                    },
                    'other_group_name': {}
                },
                **other_input_data_kwargs
            }

        when:
            - "group_name" is `StatesGroup` name
            - "state_name" is `State` name

        :param input_data: The data to check
        :type input_data: Dict

        :return: Valid input_data
        :rtype: Dict[str, Dict]
        """

        if cls.check_tag_data("dialogs", input_data, data_type=Dict):
            dialogs_data = input_data["dialogs"]

            for group_name, dialog_data in dialogs_data.items():
                if cls.check_tag_data("windows", dialog_data, data_type=Dict):
                    windows_data = dialog_data["windows"]

                    for state_name, window_data in windows_data.items():
                        cls.check_tag_data("widgets", window_data, data_type=List)

        return True

    @classmethod
    def check_tag_data(cls, tag: str, data: Dict[str, Any], data_type: Any) -> Any:
        """Checks and gets the data for the given tag.

        :param tag: The tag to check
        :type tag: str
        :param data: The data to check
        :type data: Dict
        :param data_type: The data type to check
        :type data_type: Type[Dict]

        :return: The data for the given tag
        :rtype: Any

        :raises DialogYamlException: When the input data type is invalid
        :raises InvalidTagName: When the tag is not found in the data
        :raises InvalidTagDataType: When the data type is not valid for the given tag
        """

        if not isinstance(data, Dict):
            raise DialogYamlException(
                f"Invalid data type. Expected Dict, got {type(data)}"
            )

        result_data = data.get(tag, None)

        if not result_data:
            raise InvalidTagName(tag, "Tag {tag} does not found in data.")

        if not isinstance(result_data, data_type):
            raise InvalidTagDataType(
                tag,
                "Data from {tag} must be a "
                + f"{data_type}. Found {type(result_data)}.",
            )

        return result_data
