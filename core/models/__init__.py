from typing import Type, Union, List, Dict, Any, Optional

from pydantic import BaseModel, ValidationError

from core.exceptions import BaseModelCreationError, SubModelCreationError, DialogYamlException


class YAMLModel(BaseModel):
    _models_classes_: dict[str, Type[BaseModel]] = {}

    @classmethod
    def set_classes(cls, models_classes: dict[str, Type[BaseModel]]) -> None:
        cls._models_classes_ = models_classes

    @classmethod
    def from_data(
            cls,
            yaml_data: Dict,
            yaml_model_name: str = None
    ) -> Union[BaseModel, 'YAMLSubModel']:
        submodels = cls.check_submodels(yaml_data)
        for submodel_name, submodel in submodels.items():
            model = submodel.from_data()
            if not yaml_model_name:
                return model
            yaml_data[submodel_name] = model
        else:
            try:
                model = cls.to_model(yaml_data)
                return model
            except NotImplementedError:
                raise BaseModelCreationError(model_name=yaml_model_name, data=yaml_data)
            except ValidationError:
                raise SubModelCreationError(model_name=yaml_model_name, data=yaml_data)

    @classmethod
    def to_model(
            cls,
            data: Any
    ):
        raise NotImplementedError(data)

    @classmethod
    def check_submodels(cls, data: Union[str, Dict]) -> Dict[str, 'YAMLSubModel']:
        submodels = {}
        if isinstance(data, Dict):
            for yaml_model_name, yaml_model_data in data.items():
                yaml_model_class = cls._models_classes_.get(yaml_model_name)
                if yaml_model_class:
                    sub_model = YAMLSubModel.model_validate({
                        'yaml_model_class': yaml_model_class,
                        'yaml_model_name': yaml_model_name,
                        'yaml_model_data': yaml_model_data if yaml_model_data else {}
                    })
                    submodels[yaml_model_name] = sub_model
        return submodels


class YAMLSubModel(BaseModel):
    yaml_model_class: Type[BaseModel]
    yaml_model_name: str
    yaml_model_data: Union[str, List, Dict]

    class Config:
        arbitrary_types_allowed = True

    def from_data(self):
        return self.yaml_model_class.from_data(
            yaml_data=self.yaml_model_data,
            yaml_model_name=self.yaml_model_name
        )
