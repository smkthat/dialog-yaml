"""Global fixtures and configuration for tests."""

from typing import Generator
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_aiogram_objects():
    """Fixture for mocking aiogram objects."""
    return Mock()


@pytest.fixture
def temp_yaml_file(tmp_path) -> Generator[str, None, None]:
    """Fixture for creating temporary YAML files."""

    def _create_file(content: str, filename: str = "test.yaml"):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return str(file_path)

    yield _create_file


@pytest.fixture
def sample_yaml_content():
    """Sample YAML content for tests."""
    return {
        "simple": "key: value\nanother_key: 123",
        "complex": """
        dialogs:
          main:
            windows:
              start:
                widgets:
                  - type: text
                    content: Hello World
        """,
        "with_functions": """
        functions:
          greet:
            type: function
            code: print('Hello')
        """,
        "empty": "",
        "nested": """
        nested:
          level1:
            level2:
              value: test
        """,
        "list": """
        items:
          - item1
          - item2
          - item3
        """,
    }


@pytest.fixture
def mock_states_manager():
    """Mock states manager for tests."""
    from dialog_yml.states import YAMLStatesManager

    manager = YAMLStatesManager()
    # Clear internal state
    manager._states_groups_map_ = {}
    return manager


@pytest.fixture
def mock_model_factory():
    """Mock model factory for tests."""
    from dialog_yml.models import YAMLModelFactory

    factory = YAMLModelFactory()
    factory._models_classes = {}  # Clear before each test
    return factory


@pytest.fixture
def basic_model_data():
    """Basic test data for models."""
    return {
        "text": {"type": "text", "content": "Test text"},
        "input": {"type": "input", "label": "Enter value"},
        "select": {"type": "select", "options": ["option1", "option2"]},
        "calendar": {"type": "calendar", "format": "%Y-%m-%d"},
        "counter": {"type": "counter", "min": 0, "max": 100},
        "media": {"type": "media", "source": "image.jpg"},
        "scroll": {"type": "scroll", "items": ["item1", "item2"]},
        "kbd": {
            "type": "kbd",
            "buttons": [{"text": "Button", "callback": "action"}],
        },
    }


@pytest.fixture
def valid_states_data():
    """Valid data for testing states."""
    return {
        "dialogs": {
            "main": {"windows": {"start": {}, "step1": {}, "step2": {}}},
            "settings": {"windows": {"menu": {}}},
        }
    }


@pytest.fixture
def exception_handler():
    """Exception handler fixture."""

    def handle_exception(expected_exception=None):
        if expected_exception:
            with pytest.raises(expected_exception) as exc_info:
                yield exc_info
        else:
            yield

    return handle_exception


@pytest.fixture(autouse=True)
def setup_function_registry():
    """Auto-used fixture to ensure function registry is in a clean state."""
    from dialog_yml.models.funcs.func import function_registry

    def dummy_func(*args, **kwargs):
        pass

    # Store original state
    original_funcs = {}
    for cat_name, category in function_registry._categories_map_.items():
        original_funcs[cat_name] = dict(category._functions)

    function_registry.register(dummy_func)

    yield

    # Restore original state
    for cat_name, funcs in original_funcs.items():
        category = function_registry._categories_map_[cat_name]
        category._functions = dict(funcs)

    # Ensure notify_func is registered
    from dialog_yml.models.funcs.func import notify_func

    function_registry.notify._functions["notify_func"] = notify_func


@pytest.fixture(autouse=True)
def setup_model_factory():
    """Auto-used fixture to ensure model factory is in a clean state."""
    from dialog_yml.models import YAMLModelFactory

    original_classes = dict(YAMLModelFactory._models_classes)
    YAMLModelFactory._models_classes = {}
    yield
    YAMLModelFactory._models_classes = original_classes
