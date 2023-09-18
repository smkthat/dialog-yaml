import operator
from typing import Generic, Optional, Union

from aiogram_dialog.widgets.kbd import Checkbox, Select, Radio, Multiselect

from core.models.base import WidgetModel, T
from core.models.funcs import FuncModel
from core.models.texts import TextModel, FormatModel


class CheckboxModel(WidgetModel, Generic[T]):
    id: str
    on_state_changed: Optional[FuncModel] = None
    checked: Optional[TextModel] = TextModel(val='[✓] Checked')
    unchecked: Optional[TextModel] = TextModel(val='[ ] Unchecked')
    default: Optional[bool] = True

    def get_obj(self) -> Checkbox:
        args = [
            self.checked.get_obj(),
            self.unchecked.get_obj(),
        ]
        kwargs = dict(
            id=self.id,
            when=self.when.func if self.when else None,
            on_state_changed=self.on_state_changed.func if self.on_state_changed else None,
            default=self.default
        )
        return Checkbox(
            *args,
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'CheckboxModel':
        return cls.model_validate(data)


class SelectModel(WidgetModel, Generic[T]):
    text: Optional[Union[TextModel, FormatModel]]
    id: str
    items: Union[str, list, dict]
    item_id_getter: Union[int, str, FuncModel]
    on_click: Optional[FuncModel]

    def get_obj(self) -> Select:
        item_id_getter = self.item_id_getter
        if isinstance(item_id_getter, int):
            item_id_getter = operator.itemgetter(item_id_getter)
        else:
            item_id_getter = item_id_getter.func
        kwargs = dict(
            text=self.text.get_obj(),
            id=self.id,
            items=self.items,
            item_id_getter=item_id_getter,
            on_click=self.on_click.func if self.on_click else None,
            when=self.when.func if self.when else None,
        )
        return Select(
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'SelectModel':
        if 'format' in data:
            data['text'] = data.pop('format')
        if isinstance(data['item_id_getter'], str):
            data['item_id_getter'] = FuncModel.to_model(data['item_id_getter'])
        return cls(**data)


class RadioModel(WidgetModel, Generic[T]):
    id: str
    items: Union[str, list, dict]
    on_state_changed: Optional[FuncModel]
    checked: Optional[FormatModel] = FormatModel(val='✓ {item}')
    unchecked: Optional[FormatModel] = FormatModel(val='{item}')
    item_id_getter: Union[int, str, FuncModel]

    def get_obj(self) -> Radio:
        args = [
            self.checked.get_obj(),
            self.unchecked.get_obj(),
        ]
        item_id_getter = self.item_id_getter
        if isinstance(item_id_getter, int):
            item_id_getter = operator.itemgetter(item_id_getter)
        else:
            item_id_getter = item_id_getter.func
        kwargs = dict(
            id=self.id,
            when=self.when.func if self.when else None,
            items=self.items,
            item_id_getter=item_id_getter,
            on_state_changed=self.on_state_changed.func if self.on_state_changed else None,
        )
        return Radio(
            *args,
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'RadioModel':
        if isinstance(data['item_id_getter'], str):
            data['item_id_getter'] = FuncModel.to_model(data['item_id_getter'])
        return cls(**data)


class MultiSelectModel(SelectModel, CheckboxModel, Generic[T]):
    min_selected: Optional[int] = 0
    max_selected: Optional[int] = 0
    checked: Optional[FormatModel] = FormatModel(val='✓ {item[0]}')
    unchecked: Optional[FormatModel] = FormatModel(val='{item[0]}')

    def get_obj(self) -> Multiselect:
        item_id_getter = self.item_id_getter
        if isinstance(item_id_getter, int):
            item_id_getter = operator.itemgetter(item_id_getter)
        else:
            item_id_getter = item_id_getter.func
        kwargs = dict(
            checked_text=self.checked.get_obj(),
            unchecked_text=self.unchecked.get_obj(),
            id=self.id,
            items=self.items,
            item_id_getter=item_id_getter,
            on_state_changed=self.on_state_changed.func if self.on_state_changed else None,
            on_click=self.on_click.func if self.on_click else None,
            when=self.when.func if self.when else None,
        )
        return Multiselect(
            **kwargs
        )

    @classmethod
    def to_model(cls, data: Union[str, dict]) -> 'MultiSelectModel':
        if isinstance(data['item_id_getter'], str):
            data['item_id_getter'] = FuncModel.to_model(data['item_id_getter'])
        return cls(**data)
