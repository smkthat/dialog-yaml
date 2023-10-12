from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def data_getter(
    dialog_manager: DialogManager, *_args, **_kwargs
) -> dict[str, Any]:
    return {
        "name": dialog_manager.dialog_data.get("name", ""),
        "option": dialog_manager.find("chk").is_checked(),
        "emoji": dialog_manager.find("emoji").get_checked(),
    }


async def set_name(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    manager.dialog_data["name"] = message.text
    await manager.next()


def register_switch(registry):
    registry.func.register(data_getter)
    registry.func.register(set_name)
