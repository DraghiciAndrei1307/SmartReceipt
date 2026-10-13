from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class ReceiptItem(BaseModel):
    name: str = Field(..., description="Numele produsului de pe bon")
    quantity: float = 1.0
    price: float

class ReceiptSchema(BaseModel):
    merchant_name: Optional[str] = "Necunoscut"
    total_amount: float
    needs_review: bool = False
    items: List[ReceiptItem]

    # To solve the AI hallucination, we need to validate the data...
    @model_validator(mode='after')
    def verify_and_fix_total(self):
        if self.items:
            calculated_total = sum(item.price * item.quantity for item in self.items)
            # If the difference is above "10 bani", we use the extracted total.
            if abs(self.total_amount - calculated_total) > 0.1:
                print(f"Totalul returnat de AI: {self.total_amount} ")
                print(f"Totalul corect: {calculated_total}")
                self.total_amount = round(calculated_total, 2)
                self.needs_review = True
        return self