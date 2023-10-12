from .text import (
    TextModel,
    FormatModel,
    MultiTextModel,
    CaseModel,
    ListModel,
    TextField,
)

text_classes = dict(
    text=TextModel,
    format=FormatModel,
    multi=MultiTextModel,
    case=CaseModel,
    list=ListModel,
)
