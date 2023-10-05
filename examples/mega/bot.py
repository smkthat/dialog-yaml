import asyncio
import logging
from contextlib import suppress

import dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ErrorEvent

from aiogram_dialog import DialogManager, StartMode, ShowMode, setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from core import DialogYAMLBuilder
from core.middleware import DialogYAMLMiddleware
from examples.mega.bot import register
from examples.mega.bot.custom import CustomCalendarModel


async def start(message: Message, dialog_manager: DialogManager):
    # it is important to reset stack because the user wants to restart everything
    data = dialog_manager.middleware_data
    dialog_yaml: DialogYAMLBuilder = data['dialog_yaml']
    await dialog_manager.start(
        state=dialog_yaml.states_holder.get_by_name('Menu:MAIN'),
        mode=StartMode.RESET_STACK
    )


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    """Example of handling UnknownIntent Error and starting new dialog."""
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
        )
        try:
            await event.update.callback_query.message.delete()
        except TelegramBadRequest:
            with suppress(TelegramBadRequest):
                await event.update.callback_query.message.edit_caption(caption=' ', reply_markup=None)
            with suppress(TelegramBadRequest):
                await event.update.callback_query.message.edit_text(text=' ', reply_markup=None)
    data = dialog_manager.middleware_data
    dialog_yaml: DialogYAMLBuilder = data['dialog_yaml']
    await dialog_manager.start(
        state=dialog_yaml.states_holder.get_by_name('Menu:MAIN'),
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def main():
    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    dy_router = Router()
    dy_builder = DialogYAMLBuilder()
    dy_builder.register_custom_model('my_calendar', CustomCalendarModel)
    register(dy_builder)
    dialogs = dy_builder.build('main.yaml', 'data')
    dy_router.include_routers(*dialogs)
    dy_router.message.middleware.register(DialogYAMLMiddleware(dialog_yaml=dy_builder))
    dy_router.callback_query.middleware.register(DialogYAMLMiddleware(dialog_yaml=dy_builder))
    dy_router.errors.middleware.register(DialogYAMLMiddleware(dialog_yaml=dy_builder))
    setup_dialogs(dy_router)

    dy_router.message.register(start, F.text == "/start")
    dy_router.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(dy_router)
    bot = Bot(token=dotenv.dotenv_values().get('MEGA_BOT_TOKEN'))
    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
