from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter

from core import FuncRegistry


async def counter_getter(dialog_manager: DialogManager, **kwargs):
    counter: ManagedCounter = dialog_manager.find('counter')
    return {
        'progress': counter.get_value() / 10 * 100,
    }


async def on_text_click(
        event: CallbackQuery, widget: ManagedCounter,
        manager: DialogManager,
) -> None:
    await event.answer(f"Value: {widget.get_value()}")


def register_counters(dialog_yaml: FuncRegistry):
    dialog_yaml.func.register(counter_getter)
    dialog_yaml.func.register(on_text_click)
