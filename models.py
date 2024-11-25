from pydantic import BaseModel, Field
from typing import Optional, List


class LineItem(BaseModel):
    description: Optional[str] = Field( description="A brief description of the item.")
    quantity: Optional[str] = Field(description="The number of units for the item.")
    unit_price: Optional[str] = Field(description="The price per unit for the item.")
    line_total: Optional[str] = Field(description="The total cost for this line item (quantity * unit price).")
    taxable: Optional[str] = Field(description="Indicates if the item is taxable ('Yes' or 'No').")
    currency: Optional[str] = Field(description="The currency used for this line item (e.g., 'USD', 'EUR').")
    final_amount: Optional[str] = Field(description="The final amount after applying taxes or discounts.")

class Invoice(BaseModel):
    invoice_number: Optional[str] = Field(description="The unique identifier for the invoice.")
    invoice_date: Optional[str] = Field(description="The date when the invoice was issued.")
    due_date: Optional[str] = Field(description="The deadline for payment.")
    currency: Optional[str] = Field(description="The currency used for the invoice totals (e.g., 'USD').")
    total_amount_with_tax: Optional[str] = Field(description="The total amount including all applicable taxes.")
    total_amount_without_tax: Optional[str] = Field(description="The total amount excluding taxes.")
    invoiced_office: Optional[str] = Field(description="The office responsible for invoicing.")
    supplier_name: Optional[str] = Field(description="The name of the supplier or company issuing the invoice.")
    line_items: List[LineItem] = Field(default_factory=list, description="A list of line items included in the invoice.")
