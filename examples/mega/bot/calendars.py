from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCalendar

from core import FuncRegistry


async def on_date_selected(
        callback: CallbackQuery,
        widget: ManagedCalendar,
        manager: DialogManager,
        selected_date: date,
):
    await callback.answer(str(selected_date))


def register_calendars(dialog_yaml: FuncRegistry):
    dialog_yaml.func.register(on_date_selected)
