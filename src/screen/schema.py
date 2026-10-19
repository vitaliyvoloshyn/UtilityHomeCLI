from typing import Any

from pydantic import BaseModel


class ComponentDTO(BaseModel):
    action: str = ""
    params: dict = {}
    payload: dict[str, Any] = {}
