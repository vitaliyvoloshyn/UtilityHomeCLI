from __future__ import annotations

from typing import ClassVar, Generic, TypeVar

from pydantic import BaseModel

from .client import APIClient

CreateModelT = TypeVar("CreateModelT", bound=BaseModel)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseModel)
ResponseModelT = TypeVar("ResponseModelT", bound=BaseModel)


class BaseResourceAPI(Generic[CreateModelT, UpdateModelT, ResponseModelT]):
    """Універсальний CRUD-шар над APIClient."""

    endpoint: ClassVar[str]
    response_model: ClassVar[type[ResponseModelT]]

    def __init__(self, client: APIClient = APIClient) -> None:
        self.client = client()

    def list(self) -> list[ResponseModelT]:
        response = self.client.request("GET", self.endpoint)
        data = response.json()
        if not isinstance(data, list):
            raise TypeError(
                f"Expected a list from {self.endpoint}, got {type(data).__name__}"
            )
        return [self.response_model.model_validate(item) for item in data]

    def get(self, resource_id: int) -> ResponseModelT:
        response = self.client.request("GET", self._resource_url(resource_id))
        return self.response_model.model_validate(response.json())

    def create(self, payload: CreateModelT) -> ResponseModelT:
        response = self.client.request(
            "POST",
            self.endpoint,
            json=payload.model_dump(exclude_unset=True),
        )
        return self.response_model.model_validate(response.json())

    def update(self, resource_id: int, payload: UpdateModelT) -> ResponseModelT:
        response = self.client.request(
            "PATCH",
            self._resource_url(resource_id),
            json=payload.model_dump(exclude_unset=True),
        )
        return self.response_model.model_validate(response.json())

    def replace(self, resource_id: int, payload: UpdateModelT) -> ResponseModelT:
        response = self.client.request(
            "PUT",
            self._resource_url(resource_id),
            json=payload.model_dump(exclude_unset=True),
        )
        return self.response_model.model_validate(response.json())

    def delete(self, resource_id: int) -> None:
        self.client.request("DELETE", self._resource_url(resource_id))

    def _resource_url(self, resource_id: int) -> str:
        return f"{self.endpoint.rstrip('/')}/{resource_id}/"
