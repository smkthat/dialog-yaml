from .select import CheckboxModel, SelectModel, RadioModel, MultiSelectModel

select_classes = dict(
    checkbox=CheckboxModel,
    select=SelectModel,
    radio=RadioModel,
    multi_select=MultiSelectModel,
    multiselect=MultiSelectModel,
)
