from .text import (
    TextModel,
    FormatModel,
    MultiTextModel,
    CaseModel,
    ListModel
)

text_classes = dict(
    text=TextModel,
    format=FormatModel,
    multi=MultiTextModel,
    case=CaseModel,
    list=ListModel
)
