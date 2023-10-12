import asyncio
import logging
from contextlib import suppress

from dotenv import load_dotenv, dotenv_values
from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ErrorEvent

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent

from core import DialogYAMLBuilder, FuncsRegistry
from examples.mega.bot import register_dialog_yaml_funcs
from examples.mega.bot.custom import CustomCalendarModel


async def start(message: Message, dialog_manager: DialogManager):
    # it is important to reset stack because the user wants to restart everything
    data = dialog_manager.middleware_data
    dialog_yaml: DialogYAMLBuilder = data["dialog_yaml"]
    await dialog_manager.start(
        state=dialog_yaml.states_manager.get_by_name("Menu:MAIN"),
        mode=StartMode.RESET_STACK,
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
                await event.update.callback_query.message.edit_caption(
                    caption=" ", reply_markup=None
                )
            with suppress(TelegramBadRequest):
                await event.update.callback_query.message.edit_text(
                    text=" ", reply_markup=None
                )
    data = dialog_manager.middleware_data
    dialog_yaml: DialogYAMLBuilder = data["dialog_yaml"]
    await dialog_manager.start(
        state=dialog_yaml.states_manager.get_by_name("Menu:MAIN"),
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


class CustomSG(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    register_dialog_yaml_funcs(FuncsRegistry())
    dy_builder = DialogYAMLBuilder.build(
        yaml_file_name="main.yaml",
        yaml_dir_path="data",
        models={"my_calendar": CustomCalendarModel},
        states=[CustomSG],
        router=Router(),
    )

    dy_builder.router.message.register(start, F.text == "/start")
    dy_builder.router.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(dy_builder.router)
    bot = Bot(token=dotenv_values()["MEGA_BOT_TOKEN"])
    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
