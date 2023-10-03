from typing import Any

from pydantic import ConfigDict

from core.models import YAMLModel
from core.models.funcs import FuncField


class WidgetModel(YAMLModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='allow'
    )

    when: FuncField = None

    @classmethod
    def to_model(cls, data: Any):
        raise NotImplementedError(data)
