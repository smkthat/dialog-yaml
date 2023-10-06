import pytest
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia

from core.models.widgets.medias import StaticMediaModel, DynamicMediaModel
from test.models.widgets.conftest import TestWidgetBase


class TestMedias(TestWidgetBase):
    @pytest.mark.parametrize('input_data, expected_model_cls, expected_widget_cls', [
        ({'static_media': {
            'path': {'val': 'media/{current_page}.png', 'formatted': True},
            'when': 'test_func'
        }},
         StaticMediaModel, StaticMedia),
        ({'dynamic_media': 'selector_key'},
         DynamicMediaModel, DynamicMedia),
        ({'dynamic_media': {'selector': 'selector_key', 'when': 'test_func'}},
         DynamicMediaModel, DynamicMedia),
    ])
    def test_medias(self, input_data: dict, expected_model_cls, expected_widget_cls):
        widget_model = self.yaml_model.create_model(input_data)
        assert isinstance(widget_model, expected_model_cls)

        widget_obj = widget_model.to_object()
        assert isinstance(widget_obj, expected_widget_cls)
