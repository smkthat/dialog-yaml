from core import FuncsRegistry
from .layouts import register_layouts
from .scrolls import register_scrolls
from .selects import register_selects
from .counters import register_counters
from .multiwidgets import register_multiwidgets
from .switch import register_switch
from .calendars import register_calendars


def register_dialog_yaml_funcs(registry: FuncsRegistry):
    register_switch(registry)
    register_multiwidgets(registry)
    register_selects(registry)
    register_scrolls(registry)
    register_counters(registry)
    register_layouts(registry)
    register_calendars(registry)
