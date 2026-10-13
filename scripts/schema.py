from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    name: Optional[str] = Field(
        default="Produs necunoscut",
        description="Numele produsului"
    )
    quantity: Optional[float] = Field(
        default=1.0,
        description="Cantitatea"
    )
    price: Optional[float] = Field(
        default=0.0,
        description="Pret"
    )

class ReceiptSchema(BaseModel):
    merchant_name: Optional[str] = Field(
        default="Necunoscut",
        description="Numele magazinului"
    )
    date: Optional[str] = Field(
        default=None,
        description="Data de pe bon"
    )
    total_amount: Optional[float] = Field(
        default=0.0,
        description="Suma totala"
    )
    items: List[LineItem] = Field(
        default=[],
        description="Lista produselor"
    )
