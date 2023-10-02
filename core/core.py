import logging
import os
from typing import Type

from aiogram_dialog import Dialog
from pydantic import BaseModel


from .reader import YAMLReader
from .states import YAMLDialogStatesHolder
from .models import YAMLModel
from .models.base import WidgetModel
from .models.window import WindowModel
from .models.dialog import DialogModel
from .models.funcs import function_registry, FuncRegistry, func_classes
from .models.widgets import widget_classes


logger = logging.getLogger(__name__)


models_classes = dict(
    window=WindowModel,
    dialog=DialogModel,
    **func_classes,
    **widget_classes
)


class DialogYAMLBuilder:
    func_registry: FuncRegistry = function_registry
    states_holder: YAMLDialogStatesHolder = YAMLDialogStatesHolder()
    model_parser = YAMLModel
    model_parser.set_classes(models_classes)

    @property
    def func(self):
        return self.func_registry.func

    @classmethod
    def register_custom_model(cls, yaml_tag: str, custom_model: Type[YAMLModel]):
        logger.debug(f'Register tag {yaml_tag!r} for model {custom_model.__name__!r}')
        cls.model_parser._add_model_class(yaml_tag, custom_model)

    @classmethod
    def build(cls, yaml_file_name: str, yaml_dir_path: str = None) -> list[Dialog]:
        logger.debug('Build dialogs')
        data = YAMLReader.read_data_to_dict(data_file_path=yaml_file_name, data_dir_path=yaml_dir_path)
        data_file_path = os.path.join(yaml_dir_path, yaml_file_name)

        if data:
            dialog_models = {}
            cls.states_holder.load_data(data)
            dialogs_data = data.get('dialogs')

            if not dialogs_data or not isinstance(dialogs_data, dict):
                raise TypeError('Tag \'dialogs\' must be a non-empty dict.')

            for group_name, dialog_model_data in dialogs_data.items():
                if dialog_model_data:
                    try:
                        dialog_model_data['windows'] = cls._build_windows(group_name, dialog_model_data['windows'])
                        dialog_models[group_name] = DialogModel.from_data(dialog_model_data)

                    except KeyError as e:
                        raise ValueError(f'Tag "{e.args[0]}" not found in dialogs["{group_name}"].')
                    except ValueError as e:
                        raise ValueError(f'Invalid value for dialogs["{group_name}"]["windows"]: {e}')

                else:
                    raise RuntimeError(f'Dialogs data not provided in {data_file_path!r}.')

            dialogs = cls._build_dialogs(dialog_models)
            cls.dialogs = dialogs
            return dialogs
        else:
            raise RuntimeError(f'YAML data file {data_file_path!r} not provided!')

    @classmethod
    def _register_states_(cls, data: dict):
        print(data)

    @classmethod
    def _build_dialogs(cls, dialog_models: dict) -> list[Dialog]:
        logger.debug('Build dialogs')
        dialogs = [dialog_model.get_obj() for dialog_model in dialog_models.values()]
        return dialogs

    @classmethod
    def _build_widget(cls, widget_data: dict):
        widget = WidgetModel.from_data(widget_data)
        return widget

    @classmethod
    def _build_widgets(cls, widgets_data: list[dict], state_group_raw: str):
        logger.debug(f'Build widgets for {state_group_raw!r} window')
        widgets = [cls._build_widget(widget_data) for widget_data in widgets_data]
        return widgets

    @classmethod
    def _build_window(cls, group_name: str, state_name: str, window_data: dict) -> BaseModel:
        state_group_raw = f'{group_name}:{state_name}'
        window_data['state'] = state_group_raw
        window_data['widgets'] = cls._build_widgets(window_data.get('widgets', []), state_group_raw)
        window_model = WidgetModel.from_data(dict(window=window_data))
        return window_model

    @classmethod
    def _build_windows(cls, group_name, windows_data):
        logger.debug(f'Build windows for {group_name!r} dialog')
        if windows_data and isinstance(windows_data, dict):
            return [
                cls._build_window(group_name, state_name, window_data)
                for state_name, window_data in windows_data.items()
            ]

        raise ValueError('Tag \'windows\' must be a non-empty dict')
