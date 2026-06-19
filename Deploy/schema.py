from pydantic import BaseModel

class RevenueRequest(BaseModel):
    Sales_Qunatity: int
    Customers: int
    Margin: float
    Margin_Goal: float
    Revenue_Goal: float
    Date: str
    Department: str
    Seller: str