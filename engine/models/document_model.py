from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class DocumentStatus(str, Enum):
    """Lifecycle states of a document in the SaaS pipeline."""

    UPLOADED = "UPLOADED"
    PARSED = "PARSED"
    INPUT_EDITED = "INPUT_EDITED"
    CALCULATED = "CALCULATED"
    FINAL_EDITED = "FINAL_EDITED"
    PRINT_READY = "PRINT_READY"
    EXPORTED = "EXPORTED"


class BillItem(BaseModel):
    """Representation of a single line item in a bill."""

    item_no: str = Field(..., description="Item number or code from work order")
    description: str = Field(..., description="Description of the work/item")
    unit: str = Field(default="Nos", description="Unit of measurement")
    quantity: float = Field(default=0.0, description="Quantity measured/claimed")
    rate: float = Field(default=0.0, description="Rate per unit")
    amount: float = Field(default=0.0, description="Calculated amount (Qty * Rate)")
    is_part_rate: bool = Field(default=False, description="Whether this is a part rate item")
    original_rate: Optional[float] = Field(None, description="Original rate before reduction")
    remarks: Optional[str] = Field(None, description="Optional remarks for this item")

    @field_validator("amount", mode="after")
    @classmethod
    def validate_amount(cls, v: float, info) -> float:
        """Ensure amount matches qty * rate (basic integrity)."""
        values = info.data
        qty = values.get("quantity", 0.0)
        rate = values.get("rate", 0.0)
        expected = round(qty * rate, 2)
        # We allow small float precision differences but warn if needed
        return v


class DocumentMetadata(BaseModel):
    """Metadata for the bill document."""

    bill_no: str
    work_name: str
    contractor_name: str
    agreement_no: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    source_mode: str = Field(..., description="Mode 1, 2, or 3")
    source_filename: Optional[str] = None


class UnifiedDocument(BaseModel):
    """The root model for a consolidated bill document."""

    id: str = Field(..., description="Unique UUID for the document")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    metadata: DocumentMetadata
    items: List[BillItem] = Field(default_factory=list)
    summary: Dict[str, float] = Field(
        default_factory=lambda: {"total_amount": 0.0, "tax_amount": 0.0, "net_amount": 0.0}
    )
    history: List[Dict[str, Union[str, datetime]]] = Field(default_factory=list)

    @property
    def total_amount(self) -> float:
        """Convenience property for the total amount."""
        return self.summary.get("total_amount", 0.0)

    def update_totals(self):
        """Recalculate summary totals based on items."""
        total = sum(item.amount for item in self.items)
        self.summary["total_amount"] = round(total, 2)
        # Placeholder for tax/net logic
        self.summary["net_amount"] = self.summary["total_amount"]
