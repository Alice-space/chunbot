from typing import Literal, TypedDict, Optional, TypeAlias

ImportanceType: TypeAlias = Literal["一般", "无关", "重要", "未分配"]

class News(TypedDict):
    success: bool
    error_msg: Optional[str]

    source: str
    title: Optional[str]
    summary: Optional[str]
    importance: ImportanceType
    url: Optional[str]  # Must be a complete URL