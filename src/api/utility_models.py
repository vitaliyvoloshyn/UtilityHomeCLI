from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from .base_model import APIModel
from .models import CategoryResponse


class BenefitType(StrEnum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class ChargeType(StrEnum):
    FIXED_MONTHLY = "fixed_monthly"
    BY_METER = "by_meter"
    ONE_TIME = "one_time"


class MeterCreate(APIModel):
    account: int
    category: int
    unit_of_measure: str | None = Field(default=None, max_length=20)


class MeterUpdate(APIModel):
    account: int | None = None
    category: int | None = None
    unit_of_measure: str | None = Field(default=None, max_length=20)


class MeterResponse(MeterCreate):
    id: int
    category_details: CategoryResponse


class MeterReadingCreate(APIModel):
    meter: int
    reading_value: Decimal = Field(..., max_digits=12, decimal_places=3)
    reading_date: date
    is_estimated: bool = False


class MeterReadingUpdate(APIModel):
    meter: int | None = None
    reading_value: Decimal | None = Field(default=None, max_digits=12, decimal_places=3)
    reading_date: date | None = None
    is_estimated: bool | None = None


class MeterReadingResponse(MeterReadingCreate):
    id: int
    consumption: str


class TariffCreate(APIModel):
    provider: int
    name: str = Field(..., max_length=150)
    charge_type: ChargeType
    price_per_unit: Decimal = Field(..., max_digits=10, decimal_places=4)
    effective_from: date


class TariffUpdate(APIModel):
    provider: int | None = None
    name: str | None = Field(default=None, max_length=150)
    charge_type: ChargeType | None = None
    price_per_unit: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=4
    )
    effective_from: date | None = None
    effective_to: date | None = None


class TariffResponse(TariffCreate):
    id: int
    charge_type_display: str


class BenefitCreate(APIModel):
    account: int
    name: str = Field(..., max_length=150)
    benefit_type: BenefitType
    discount_value: Decimal = Field(..., max_digits=10, decimal_places=2)
    effective_from: date
    effective_to: date | None = None
    is_active: bool = True


class BenefitUpdate(APIModel):
    account: int | None = None
    name: str | None = Field(default=None, max_length=150)
    benefit_type: BenefitType | None = None
    discount_value: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2
    )
    effective_from: date | None = None
    effective_to: date | None = None
    is_active: bool | None = None


class BenefitResponse(BenefitCreate):
    id: int
    benefit_type_display: str
