from typing import Union, Self

from aiogram.enums import ContentType
from aiogram_dialog.widgets.input import MessageInput
from pydantic import field_validator

from core.models.base import WidgetModel
from core.models.funcs import FuncField
from core.utils import clean_empty


class MessageInputModel(WidgetModel):
    func: FuncField
    filter: FuncField = None
    content_types: list[ContentType] = [ContentType.ANY]

    def to_object(self) -> MessageInput:
        kwargs = clean_empty(
            dict(
                func=self.func.func if self.func else None,
                filter=self.filter.func if self.filter else None,
                content_types=self.content_types,
            )
        )
        return MessageInput(**kwargs)

    @field_validator("content_types", mode="before")
    def validate_content_types(cls, value):
        if not value:
            return None

        if isinstance(value, str):
            value = [value]

        result = []
        if isinstance(value, list):
            for v in value:
                if isinstance(v, ContentType):
                    result.append(v)
                elif isinstance(v, str):
                    result.append(ContentType[v.upper()])
                else:
                    return None

        return result

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)
