from pydantic import BaseModel




class AddressBase(BaseModel):
    municipality: str
    city: str
    country: str
    postal_code: int
    
class AddressOut(AddressBase):
    id: str
    user_id : str
