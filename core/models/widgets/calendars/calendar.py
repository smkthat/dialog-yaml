from typing import Union, Self

from aiogram_dialog.widgets.kbd import Calendar

from core.models.base import WidgetModel
from core.models.funcs import FuncField
from core.utils import clean_empty


class CalendarModel(WidgetModel):
    id: str = None
    on_click: FuncField = None

    def to_object(self) -> Calendar:
        kwargs = clean_empty(dict(
            id=self.id,
            on_click=self.on_click.func if self.on_click else None,
            when=self.when.func if self.when else None
        ))
        return Calendar(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'id': data}
        return cls(**data)
