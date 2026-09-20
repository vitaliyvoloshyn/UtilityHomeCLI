from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    """Base Pydantic model used by API request and response schemas."""

    model_config = ConfigDict(extra="ignore")
