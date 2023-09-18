from typing import (Union, Generic, Optional, Any)

from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List

from core.models.base import WidgetModel, T
from core.models.funcs import FuncModel


class TextModel(WidgetModel, Generic[T]):
    val: str

    def get_obj(self) -> Const:
        kwargs = dict(
            when=self.when.func if self.when else None,
            text=self.val
        )
        return Const(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'TextModel':
        if isinstance(data, str):
            data = {'val': data}
        return TextModel(**data)

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> 'TextModel':
        pass


class FormatModel(TextModel, Generic[T]):
    def get_obj(self) -> Format:
        kwargs = dict(
            when=self.when.func if self.when else None,
            text=self.val
        )
        return Format(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'FormatModel':
        if isinstance(data, str):
            data = {'val': data}
        return FormatModel(**data)


class MultiTextModel(WidgetModel):
    texts: list[TextModel]
    sep: Optional[str] = '\n'

    # TODO: Implement getter

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
    def to_model(cls, data: dict):
        if texts := data.get('texts'):
            data['texts'] = [cls.from_data(text_data) for text_data in texts]
        return cls(**data)


class CaseModel(WidgetModel):
    texts: dict[Any, FormatModel]
    selector: Union[str, FuncModel]

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
    def to_model(cls, data: dict):
        if 'texts' in data:
            data['texts'] = {
                item: FormatModel.to_model(value)
                for item, value in data['texts'].items()
            }
        if 'selector' in data and isinstance(data['selector'], dict):
            data['selector'] = cls.from_data(data['selector'])
        return cls(**data)


class ListModel(WidgetModel):
    field: FormatModel
    items: Union[str, list, dict, FuncModel]
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
    def to_model(cls, data: dict) -> 'ListModel':
        data['field'] = FormatModel.to_model(data['field'])
        if isinstance(data['items'], str):
            data['items'] = FuncModel.to_model(data['items'])
        if isinstance(data['items'], dict):
            data['items'] = cls.from_data(data['items'])
        return cls(**data)
