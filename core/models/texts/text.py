from typing import (Union, Generic, Optional, Any, Annotated, Self)

from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from pydantic import BeforeValidator

from core.models.base import WidgetModel, T
from core.models.funcs import FuncModel, FuncField


class TextModel(WidgetModel, Generic[T]):
    val: str

    def get_obj(self) -> Const:
        kwargs = dict(
            when=self.when.func if self.when else None,
            text=self.val
        )
        return Const(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            data = {'val': data}
        return cls(**data)


TextField = Annotated[TextModel, BeforeValidator(TextModel.to_model)]


class FormatModel(TextModel, Generic[T]):
    def get_obj(self) -> Format:
        kwargs = dict(
            when=self.when.func if self.when else None,
            text=self.val
        )
        return Format(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, str):
            data = {'val': data}
        return cls(**data)


class MultiTextModel(WidgetModel):
    texts: list[TextField]
    sep: Optional[str] = '\n'

    def get_obj(self) -> Multi:
        kwargs = dict(
            when=self.when.func if self.when else None,
            sep=self.sep
        )
        return Multi(
            *[text.get_obj() for text in self.texts],
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return Self
        if texts := data.get('texts'):
            data['texts'] = [cls.from_data(text_data) for text_data in texts]
        return cls(**data)


class CaseModel(WidgetModel):
    texts: dict[Any, TextField]
    selector: Union[str, FuncField]

    def get_obj(self) -> Case:
        kwargs = dict(
            texts={item: value.get_obj() for item, value in self.texts.items()},
            selector=self.selector.func if isinstance(self.selector, FuncModel) else self.selector,
            when=self.when.func if self.when else None,
        )
        return Case(
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        if texts := data.get('texts'):
            data['texts'] = {
                item: FormatModel.to_model(text_data)
                for item, text_data in texts.items()
            }
        if 'selector' in data and isinstance(data['selector'], dict):
            data['selector'] = cls.from_data(data['selector'])
        return cls(**data)


class ListModel(WidgetModel):
    field: FormatModel
    items: Union[str, list, FuncField, dict]
    sep: Optional[str] = "\n"

    def get_obj(self) -> List:
        kwargs = dict(
            field=self.field.get_obj(),
            items=self.items.func if isinstance(self.items, FuncModel) else self.items,
            sep=self.sep,
            when=self.when.func if self.when else None
        )
        return List(
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        data['field'] = FormatModel.to_model(data['field'])
        if isinstance(data['items'], str):
            data['items'] = FuncModel.to_model(data['items'])
        if isinstance(data['items'], dict):
            data['items'] = cls.from_data(data['items'])
        return cls(**data)
