from typing import Union, Self

from aiogram_dialog import LaunchMode, Dialog
from pydantic import field_validator

from core.models.funcs import FuncField
from core.models.base import WidgetModel
from core.utils import clean_empty


class DialogModel(WidgetModel):
    windows: list[WidgetModel]
    on_start: FuncField = None
    on_close: FuncField = None
    on_process_result: FuncField = None
    launch_mode: LaunchMode = LaunchMode.STANDARD
    getter: FuncField = None
    preview_data: FuncField = None

    def get_obj(self) -> Dialog:
        kwargs = clean_empty(dict(
            on_start=self.on_start.func if self.on_start else None,
            on_close=self.on_close.func if self.on_close else None,
            on_process_result=self.on_process_result.func if self.on_process_result else None,
            launch_mode=self.launch_mode,
            getter=self.getter.func if self.getter else None,
            preview_data=self.preview_data.func if self.getter else None
        ))
        return Dialog(
            *[window.get_obj() for window in self.windows],
            **kwargs
        )

    @field_validator('launch_mode', mode='before')
    def validate_launch_mode(cls, value) -> LaunchMode:
        if isinstance(value, LaunchMode):
            return value
        if isinstance(value, str):
            return LaunchMode[value.upper()]

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)
