import os
import yaml

from typing import Dict
from yamlinclude import YamlIncludeConstructor

from .models.selects import select_classes
from .states import YAMLDialogStatesHolder
from .models import YAMLModel
from .models.base import WidgetModel
from .models.funcs import func_classes
from .models.texts import text_classes


class YAMLReader:
    @classmethod
    def read_data_to_dict(cls, data_file_path: str, data_dir_path: str = None) -> Dict:
        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader,
            base_dir=data_dir_path
        )
        abs_data_file_path = os.path.abspath(os.path.join(data_dir_path, data_file_path))
        with open(abs_data_file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data


models_classes = dict(
        **func_classes,
        **text_classes,
        **select_classes,
    )


class YAMLDialogBuilder:
    states_holder: YAMLDialogStatesHolder = YAMLDialogStatesHolder()
    model_parser = YAMLModel
    model_parser.set_classes(models_classes)

    @classmethod
    def register_custom_class(cls, yaml_key: str, custom_class):
        if yaml_key not in cls.model_parser._models_classes_:
            cls.model_parser._models_classes_[yaml_key] = custom_class
        else:
            key_class = cls.model_parser._models_classes_[yaml_key]
            raise RuntimeError(f'Custom class key={yaml_key!r} already in use by model class={key_class.__name__}')

    @classmethod
    def build(cls, yaml_file_name: str, yaml_dir_path: str = None):
        data = YAMLReader.read_data_to_dict(data_file_path=yaml_file_name, data_dir_path=yaml_dir_path)
        data_file_path = os.path.join(yaml_dir_path, yaml_file_name)

        if data:
            cls.states_holder.load_data(data)
            dialogs_data = data.get('dialogs')
            if dialogs_data:
                dialog_kwargs = {}
                for state_group_name, dialog_data in dialogs_data.items():
                    for key, data in dialog_data.items():
                        if key == 'windows':
                            for state_name, window_data in data.items():
                                state_key = f'{state_group_name}:{state_name}'
                                state = cls.states_holder.get(state_key)
                                window_kwargs = {}
                                for window_key, w_data in window_data.items():
                                    if window_key == 'widgets':
                                        widgets = []
                                        for widget_data in w_data:
                                            widget = cls.model_parser.from_data(widget_data)
                                            widgets.append(widget)
                                    else:
                                        window_kwargs.update({window_key: w_data})

                        elif key == 'anchors':
                            continue
                        else:
                            dialog_kwargs.update({key: data})

            else:
                raise RuntimeError(f'Dialogs data not provided in {data_file_path!r}.')
        else:
            raise RuntimeError(f'YAML data file {data_file_path!r} not provided!')

    @classmethod
    def _register_states_(cls, data: dict):
        print(data)

    @classmethod
    def _build_model_(cls, model_class, model_data: dict) -> WidgetModel:
        model = model_class.to_model(model_data)
        return model
