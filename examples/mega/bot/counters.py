from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter

from core import FuncsRegistry


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


def register_counters(registry: FuncsRegistry):
    registry.func.register(counter_getter)
    registry.func.register(on_text_click)
