from __future__ import annotations

from datetime import date

from pydantic import Field

from .base_model import APIModel


class PropertyCreate(APIModel):
    """Payload for creating a property."""

    address: str
    name: str = Field(max_length=100)


class PropertyUpdate(APIModel):
    """Payload for partially updating a property."""

    address: str | None = None
    name: str | None = Field(default=None, max_length=100)


class PropertyResponse(PropertyCreate):
    id: int
    user: int


class ProviderCreate(APIModel):
    """Payload for creating a service provider."""

    name: str = Field(..., max_length=255)
    edrpou: str | None = Field(default=None, max_length=10)
    contact_info: str | None = None


class ProviderUpdate(APIModel):
    name: str | None = Field(default=None, max_length=255)
    edrpou: str | None = Field(default=None, max_length=10)
    contact_info: str | None = None


class ProviderResponse(ProviderCreate):
    id: int


class CategoryCreate(APIModel):
    name: str = Field(..., max_length=100)
    unit_of_measure: str | None = Field(default=None, max_length=20)


class CategoryUpdate(APIModel):
    name: str | None = Field(default=None, max_length=100)
    unit_of_measure: str | None = Field(default=None, max_length=20)


class CategoryResponse(CategoryCreate):
    id: int


class AccountNumberCreate(APIModel):
    property: int
    provider: int
    account_number: str = Field(..., max_length=50)


class AccountNumberUpdate(APIModel):
    property: int | None = None
    provider: int | None = None
    account_number: str | None = Field(default=None, max_length=50)


class AccountNumberResponse(AccountNumberCreate):
    id: int
    created_at: date
    property_details: PropertyResponse
    provider_details: ProviderResponse


class UserResponse(APIModel):
    """Authenticated user returned by the API."""

    id: int | None = None
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
