import calendar

from aiogram_dialog import DialogManager

from src import FuncsRegistry


async def product_getter(**_kwargs):
    return {
        "products": [(f"Product {i}", i) for i in range(1, 30)],
    }


async def paging_getter(dialog_manager: DialogManager, **_kwargs):
    current_page = await dialog_manager.find("stub_scroll").get_page()
    return {
        "pages": 7,
        "current_page": current_page + 1,
        "day": calendar.day_name[current_page],
    }


def register_scrolls(registry: FuncsRegistry):
    registry.func.register(product_getter)
    registry.func.register(paging_getter)
