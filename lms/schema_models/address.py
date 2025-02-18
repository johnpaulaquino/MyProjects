from pydantic import BaseModel



class BaseAddressSchema(BaseModel):
    user_id: str
    barangay: str
    municipality: str
    province: str
    country: str
    postal_code: str
    
    
    
