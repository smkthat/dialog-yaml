from .scroll import (
    ScrollingTextModel,
    SwitchPageModel,
    StubScrollModel,
    NumberedPagerModel,
    FirstPageModel,
    PrevPageModel,
    CurrentPageModel,
    NextPageModel,
    LastPageModel
)

scroll_classes = dict(
    scrolling_text=ScrollingTextModel,
    stub_scroll=StubScrollModel,
    numbered_pager=NumberedPagerModel,
    first_page=FirstPageModel,
    prev_page=PrevPageModel,
    current_page=CurrentPageModel,
    next_page=NextPageModel,
    last_page=LastPageModel,
)
