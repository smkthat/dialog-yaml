import pytest
from aiogram_dialog.widgets.kbd import StubScroll, NumberedPager, SwitchPage
from aiogram_dialog.widgets.text import ScrollingText

from dialog_yml.models.widgets.scrolls.scroll import (
    ScrollingTextModel,
    StubScrollModel,
    NumberedPagerModel,
    FirstPageModel,
    PrevPageModel,
    CurrentPageModel,
    NextPageModel,
    LastPageModel,
)
from tests.models.widgets.conftest import TestWidgetBase


class TestScroll(TestWidgetBase):
    @pytest.mark.parametrize(
        "input_data, expected_model_cls, expected_widget_cls",
        [
            (
                {"numbered_pager": "scroll_no_pager"},
                NumberedPagerModel,
                NumberedPager,
            ),
            (
                {
                    "numbered_pager": {
                        "scroll": "scroll_no_pager",
                        "page_text": "{target_page1}\ufe0f\u20e3",
                        "current_page_text": "{current_page1}",
                    }
                },
                NumberedPagerModel,
                NumberedPager,
            ),
            (
                {
                    "scrolling_text": {
                        "text": "MJHBAa akjdkawjn dajndskjn akjdn kadn kadnk njdn kand kjs nkajnwk j",
                        "id": "text_scroll",
                        "page_size": 1000,
                    }
                },
                ScrollingTextModel,
                ScrollingText,
            ),
            (
                {"stub_scroll": {"id": "stub_scroll", "pages": "pages"}},
                StubScrollModel,
                StubScroll,
            ),
            (
                {"stub_scroll": {"id": "stub_scroll", "pages": "pages"}},
                StubScrollModel,
                StubScroll,
            ),
            ({"first_page": "scroll_no_pager"}, FirstPageModel, SwitchPage),
            ({"next_page": "scroll_no_pager"}, NextPageModel, SwitchPage),
            ({"current_page": "scroll_no_pager"}, CurrentPageModel, SwitchPage),
            ({"prev_page": "scroll_no_pager"}, PrevPageModel, SwitchPage),
            ({"last_page": "scroll_no_pager"}, LastPageModel, SwitchPage),
        ],
    )
    def test_scroll(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
