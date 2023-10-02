from typing import Generic, Union, Self, Any

from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from pydantic import field_validator

from core.models.base import WidgetModel, T
from core.models.widgets.texts import TextField
from core.utils import clean_empty


class StaticMediaModel(WidgetModel, Generic[T]):
    path: TextField = None
    uri: TextField = None
    type: ContentType = ContentType.PHOTO
    use_pipe: bool = False
    media_params: dict[str, Any] = None

    def get_obj(self) -> StaticMedia:
        kwargs = clean_empty(dict(
            path=self.path.get_obj() if self.path else None,
            url=self.uri.get_obj() if self.uri else None,
            type=self.type,
            use_pipe=self.use_pipe,
            media_params=self.media_params,
            when=self.when.func if self.when else None
        ))
        return StaticMedia(**kwargs)

    @field_validator('type', mode='before')
    def validate_type(cls, value: Union[str, ContentType]) -> ContentType:
        if isinstance(value, ContentType):
            return value

        return ContentType[value.upper()]

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)


class DynamicMediaModel(WidgetModel, Generic[T]):
    selector: str

    def get_obj(self) -> DynamicMedia:
        kwargs = clean_empty(dict(
            when=self.when.func if self.when else None,
            selector=self.selector
        ))
        obj = DynamicMedia(**kwargs)
        return obj

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = dict(selector=data)
        return cls(**data)
