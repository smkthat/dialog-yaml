import pytest
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia

from conftest import TestWidgetBase
from core.models.widgets.medias import StaticMediaModel, DynamicMediaModel


class TestMedias(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'static_media': {
            'path': {'val': 'media/{current_page}.png', 'formatted': True},
            'when': 'func_test'
        }},
         StaticMediaModel, StaticMedia),
        ({'dynamic_media': 'selector_key'},
         DynamicMediaModel, DynamicMedia),
        ({'dynamic_media': {'selector': 'selector_key', 'when': 'func_test'}},
         DynamicMediaModel, DynamicMedia),
    ])
    def test_medias(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.model_parser_class.from_data(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.get_obj()
        assert isinstance(widget_obj, expected_widget_cls)
