import os
import yaml

from aiogram_dialog import Dialog
from yamlinclude import YamlIncludeConstructor

from .models import YAMLModel
from .models.base import WidgetModel
from .models.funcs import func_classes
from .models.texts import text_classes
from .models.selects import select_classes
from .models.kbd import keyboard_classes
from .models.window import WindowModel
from .models.dialog import DialogModel
from .states import YAMLDialogStatesHolder


class YAMLReader:
    @classmethod
    def read_data_to_dict(cls, data_file_path: str, data_dir_path: str = None) -> dict:
        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader,
            base_dir=data_dir_path
        )
        abs_data_file_path = os.path.abspath(os.path.join(data_dir_path, data_file_path))
        with open(abs_data_file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data


models_classes = dict(
    window=WindowModel,
    dialog=DialogModel,
    **func_classes,
    **text_classes,
    **select_classes,
    **keyboard_classes,
)


class YAMLDialogBuilder:
    states_holder: YAMLDialogStatesHolder = YAMLDialogStatesHolder()
    model_parser = YAMLModel
    model_parser.set_classes(models_classes)

    @classmethod
    def register_custom_class(cls, yaml_key: str, custom_class):
        if yaml_key not in cls.model_parser.models_classes:
            cls.model_parser.models_classes[yaml_key] = custom_class
        else:
            key_class = cls.model_parser.models_classes[yaml_key]
            raise RuntimeError(f'Custom class key={yaml_key!r} already in use by model class={key_class.__name__}')

    @classmethod
    def build(cls, yaml_file_name: str, yaml_dir_path: str = None):
        data = YAMLReader.read_data_to_dict(data_file_path=yaml_file_name, data_dir_path=yaml_dir_path)
        data_file_path = os.path.join(yaml_dir_path, yaml_file_name)

        if data:
            dialog_models = {}
            cls.states_holder.load_data(data)
            dialogs_data = data.get('dialogs')

            if not dialogs_data or not isinstance(dialogs_data, dict):
                raise TypeError('Key "dialogs" must be a non-empty dict.')

            for group_name, dialog_model_data in dialogs_data.items():
                if dialog_model_data:
                    try:
                        windows_data = dialog_model_data['windows']
                        if not isinstance(windows_data, dict) or not windows_data:
                            raise ValueError('Key "windows" must be a non-empty dict.')

                        dialog_model_data['windows'] = [
                            cls._create_window(group_name, state_name, window_data)
                            for state_name, window_data in windows_data.items()
                        ]

                        dialog_models[group_name] = DialogModel.from_data(dialog_model_data)

                    except KeyError as e:
                        raise ValueError(f'Key "{e.args[0]}" not found in dialogs["{group_name}"].')
                    except ValueError as e:
                        raise ValueError(f'Invalid value for dialogs["{group_name}"]["windows"]: {e}')

                else:
                    raise RuntimeError(f'Dialogs data not provided in {data_file_path!r}.')

                return dialog_model_data
        else:
            raise RuntimeError(f'YAML data file {data_file_path!r} not provided!')

    @classmethod
    def _register_states_(cls, data: dict):
        print(data)

    @classmethod
    def _build_model_(cls, model_class, model_data: dict) -> WidgetModel:
        model = model_class.to_model(model_data)
        return model

    @classmethod
    def _gen_dialogs_objects(cls, dialog_models: dict) -> list[Dialog]:
        dialogs = []
        for dialog_model in dialog_models.values():
            dialog = dialog_model.get_obj()
            dialogs.append(dialog)
        return dialogs

    @classmethod
    def _create_widget(cls, widget_data: dict):
        widget = WidgetModel.from_data(widget_data)
        return widget

    @classmethod
    def _create_widgets(cls, widgets_data: list[dict]):
        widgets = []
        for widget_data in widgets_data:
            widget = cls._create_widget(widget_data)
            widgets.append(widget)
        return widgets

    @classmethod
    def _create_window(cls, group_name: str, state_name: str, window_data: dict) -> WindowModel:
        window_data['state'] = f'{group_name}:{state_name}'
        window_data['widgets'] = cls._create_widgets(window_data.get('widgets', []))
        window_model = WidgetModel.from_data(dict(window=window_data))
        return window_model

# dialog_kwargs = {}
# for state_group_name, dialog_data in dialogs_data.items():
#     for key, data in dialog_data.items():
#         if key == 'windows':
#             for state_name, window_data in data.items():
#                 state_key = f'{state_group_name}:{state_name}'
#                 state = cls.states_holder.get(state_key)
#                 window_kwargs = {}
#                 for window_key, w_data in window_data.items():
#                     if window_key == 'widgets':
#                         widgets = []
#                         for widget_data in w_data:
#                             widget = cls.model_parser.from_data(widget_data)
#                             widgets.append(widget)
#                     else:
#                         window_kwargs.update({window_key: w_data})
#
#         elif key == 'anchors':
#             continue
#         else:
#             dialog_kwargs.update({key: data})
