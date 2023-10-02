from typing import Union, Self, Generic

from aiogram_dialog.widgets.kbd import StubScroll, NumberedPager, SwitchPage
from aiogram_dialog.widgets.kbd.pager import PageDirection
from aiogram_dialog.widgets.text import ScrollingText

from core.models.funcs import FuncField, FuncModel
from core.models.widgets.texts import TextField

from core.models.base import WidgetModel, T
from core.utils import clean_empty

DEFAULT_PAGER_ID = '__pager__'

DEFAULT_LAST_BUTTON_TEXT = TextField(val='>>')
DEFAULT_FIRST_BUTTON_TEXT = TextField(val='<<')
DEFAULT_PREV_BUTTON_TEXT = TextField(val='<')
DEFAULT_NEXT_BUTTON_TEXT = TextField(val='>')
DEFAULT_CURRENT_BUTTON_TEXT = TextField(val='{current_page1}', formatted=True)
DEFAULT_PAGE_TEXT = TextField(val='{target_page1}', formatted=True)
DEFAULT_CURRENT_PAGE_TEXT = TextField(val='[ {current_page1} ]', formatted=True)


class ScrollingTextModel(WidgetModel, Generic[T]):
    id: str
    text: TextField
    page_size: int = 0
    on_page_changed: FuncField = None

    def get_obj(self) -> ScrollingText:
        kwargs = clean_empty(dict(
            id=self.id,
            page_size=self.page_size,
            text=self.text.get_obj(),
            on_page_changed=self.on_page_changed.func if self.on_page_changed else None,
            when=self.when.func if self.when else None
        ))
        return ScrollingText(**kwargs)

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return data
        return cls(**data)


class StubScrollModel(WidgetModel, Generic[T]):
    id: str
    pages: Union[str, int, FuncField]
    on_page_changed: FuncField = None

    def get_obj(self) -> StubScroll:
        kwargs = clean_empty(dict(
            id=self.id,
            pages=self.pages.func if isinstance(self.pages, FuncModel) else self.pages,
            on_page_changed=self.on_page_changed.func if self.on_page_changed else None
        ))
        return StubScroll(**kwargs)

    @classmethod
    def to_model(cls, data: Union[dict, Self]) -> Self:
        if isinstance(data, cls):
            return Self
        return cls(**data)


class NumberedPagerModel(WidgetModel, Generic[T]):
    scroll: str
    id: str = DEFAULT_PAGER_ID
    page_text: TextField = DEFAULT_PAGE_TEXT
    current_page_text: TextField = DEFAULT_CURRENT_PAGE_TEXT

    def get_obj(self) -> NumberedPager:
        kwargs = clean_empty(dict(
            id=self.id,
            scroll=self.scroll,
            page_text=self.page_text.get_obj(),
            current_page_text=self.current_page_text.get_obj(),
            when=self.when.func if self.when else None
        ))
        return NumberedPager(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]):
        if isinstance(data, cls):
            return Self
        if isinstance(data, str):
            return cls(scroll=data)
        return cls(**data)


class SwitchPageModel(WidgetModel, Generic[T]):
    id: str = DEFAULT_PAGER_ID
    text: TextField
    page: Union[int, PageDirection]
    scroll: str

    def get_obj(self) -> SwitchPage:
        kwargs = clean_empty(dict(
            id=self.id,
            page=self.page,
            scroll=self.scroll,
            text=self.text.get_obj() if self.text else None,
            when=self.when.func if self.when else None
        ))
        return SwitchPage(**kwargs)

    @classmethod
    def to_model(cls, data: Union[str, dict, Self]) -> Self:
        if isinstance(data, cls):
            return Self
        if isinstance(data, str):
            return cls(scroll=data)
        return cls(**data)


class FirstPageModel(SwitchPageModel, Generic[T]):
    page: int = PageDirection.FIRST
    text: TextField = DEFAULT_FIRST_BUTTON_TEXT


class PrevPageModel(SwitchPageModel, Generic[T]):
    page: int = PageDirection.PREV
    text: TextField = DEFAULT_PREV_BUTTON_TEXT


class CurrentPageModel(SwitchPageModel, Generic[T]):
    page: int = PageDirection.IGNORE
    text: TextField = DEFAULT_CURRENT_PAGE_TEXT


class NextPageModel(SwitchPageModel, Generic[T]):
    page: int = PageDirection.NEXT
    text: TextField = DEFAULT_NEXT_BUTTON_TEXT


class LastPageModel(SwitchPageModel):
    page: int = PageDirection.LAST
    text: TextField = DEFAULT_LAST_BUTTON_TEXT
