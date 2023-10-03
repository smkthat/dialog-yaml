from dataclasses import dataclass
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from core import FuncRegistry


@dataclass
class Fruit:
    id: str
    name: str


async def getter(*args, **_kwargs):
    return {
        'fruits': [
            Fruit('1', 'Apple'),
            Fruit('2', 'Banana'),
            Fruit('3', 'Orange'),
            Fruit('4', 'Pear'),
        ]
    }


def fruit_id_getter(fruit: Fruit) -> str:
    return fruit.id


async def on_item_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        selected_item: str,
):
    await callback.answer(f'item id: {selected_item}')


def register_selects(dialog_yaml: FuncRegistry):
    dialog_yaml.func.register(getter)
    dialog_yaml.func.register(fruit_id_getter)
    dialog_yaml.func.register(on_item_selected)
