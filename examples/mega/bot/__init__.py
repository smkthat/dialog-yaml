from .layouts import register_layouts
from .scrolls import register_scrolls
from .selects import register_selects
from .counters import register_counters
from .multiwidgets import register_multiwidgets
from .switch import register_switch
from .calendars import register_calendars


def register(dialog_yaml):
    register_switch(dialog_yaml)
    register_multiwidgets(dialog_yaml)
    register_selects(dialog_yaml)
    register_scrolls(dialog_yaml)
    register_counters(dialog_yaml)
    register_layouts(dialog_yaml)
    register_calendars(dialog_yaml)
