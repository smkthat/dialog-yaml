from typing import Union, Self

from aiogram.enums import ParseMode
from aiogram_dialog import Window
from pydantic import field_validator

from core.models.base import YAMLModel, WidgetModel
from core.models.funcs import FuncField
from core.models.widgets.kbd import GroupKeyboardField
from core.states import YAMLStatesManager
from core.utils import clean_empty


class WindowModel(YAMLModel):
    widgets: list[WidgetModel]
    state: str
    getter: FuncField = None
    parse_mode: ParseMode = ParseMode.MARKDOWN
    disable_web_page_preview: bool = False
    preview_add_transitions: GroupKeyboardField = None
    preview_data: FuncField = None

    def to_object(self) -> Window:
        kwargs = clean_empty(
            dict(
                state=YAMLStatesManager().get_by_name(self.state),
                getter=self.getter.func if self.getter else None,
                parse_mode=self.parse_mode,
                disable_web_page_preview=self.disable_web_page_preview,
                preview_add_transitions=self.preview_add_transitions
                if self.preview_add_transitions
                else None,
                preview_data=self.preview_data.func if self.preview_data else None,
            )
        )
        return Window(*[widget.to_object() for widget in self.widgets], **kwargs)

    @field_validator("widgets", mode="before")
    def validate_widgets(cls, value):
        if not value:
            raise ValueError(f"Field widgets can't be empty.")
        return value

    @field_validator("parse_mode", mode="before")
    def validate_parse_mode(cls, value):
        if isinstance(value, ParseMode):
            return value
        elif isinstance(value, str):
            return ParseMode[value.upper()]
        else:
            return None

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)
