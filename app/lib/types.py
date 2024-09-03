import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, HttpUrl


class BroadcastResponse(BaseModel):
    id: int
    date: datetime.datetime
    webinar_id: int
    title: str
    internal_title: Optional[str]
    webinar_url: Optional[HttpUrl]

    class Config:
        from_attributes = True
        use_enum_values = True
        exclude_none = True

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop("exclude_none")  # type: ignore
        return super().dict(*args, exclude_none=True, **kwargs)
