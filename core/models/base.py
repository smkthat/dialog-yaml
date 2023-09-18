from typing import Optional, TypeVar, Generic

from pydantic import ConfigDict

from core.models import YAMLModel
from core.models.funcs import FuncModel

T = TypeVar('T', bound='WidgetModel')


class WidgetModel(YAMLModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    when: Optional[FuncModel] = None
