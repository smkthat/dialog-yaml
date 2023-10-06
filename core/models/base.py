from abc import ABC, abstractmethod
from typing import Any

from aiogram_dialog.api.internal import Widget
from pydantic import ConfigDict, BaseModel

from core.models.funcs import FuncField


class YAMLModel(BaseModel, ABC):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='allow'
    )

    @classmethod
    @abstractmethod
    def to_model(cls, data: Any) -> 'YAMLModel': pass

    @abstractmethod
    def to_object(self) -> Widget: pass


class WidgetModel(YAMLModel):
    def to_object(self):
        raise NotImplementedError()

    when: FuncField = None

    @classmethod
    def to_model(cls, data: Any):
        raise NotImplementedError(data)
