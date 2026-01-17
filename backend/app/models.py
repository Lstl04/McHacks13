from pydantic import BaseModel, Field, EmailStr
from pydantic_core import core_schema
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId

# Custom type for MongoDB ObjectId (Pydantic v2 compatible)
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


# ===== USER MODELS =====

class UserBase(BaseModel):
    """Base user model with common fields"""
    businessName: Optional[str] = None
    businessEmail: Optional[EmailStr] = None
    businessPhone: Optional[str] = None
    businessAddress: Optional[str] = None
    businessCategory: Optional[str] = None
    hourlyRate: Optional[float] = None
    lastInvoiceNumber: Optional[int] = 0
    pastItems: Optional[List[dict]] = []

class UserCreate(UserBase):
    """Model for creating a new user"""
    businessEmail: EmailStr  # Required for creation

class UserUpdate(UserBase):
    """Model for updating a user (all fields optional)"""
    pass

class User(UserBase):
    """Complete user model with database fields"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "businessName": "John's Contracting",
                "businessEmail": "john@example.com",
                "businessPhone": "+1-555-0123",
                "businessAddress": "123 Main St, City, State",
                "businessCategory": "Construction",
                "hourlyRate": 75.00,
                "lastInvoiceNumber": 1001
            }
        }


# ===== CLIENT MODELS =====

class ClientBase(BaseModel):
    """Base client model"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_id: Optional[str] = None  # Reference to user
    address: Optional[str] = None

class ClientCreate(ClientBase):
    """Model for creating a new client"""
    name: str  # Required
    user_id: str  # Required - which user owns this client

class ClientUpdate(ClientBase):
    """Model for updating a client"""
    pass

class Client(ClientBase):
    """Complete client model with database fields"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Acme Corporation",
                "email": "contact@acme.com",
                "user_id": "user123",
                "address": "456 Business Ave, City, State"
            }
        }


# ===== JOB MODELS =====

class JobBase(BaseModel):
    """Base job model"""
    user_id: Optional[str] = None
    client_id: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = "pending"  # pending, in_progress, completed, cancelled
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    invoice_id: Optional[str] = None

class JobCreate(JobBase):
    """Model for creating a new job"""
    user_id: str  # Required
    client_id: str  # Required
    title: str  # Required

class JobUpdate(JobBase):
    """Model for updating a job"""
    pass

class Job(JobBase):
    """Complete job model with database fields"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "client_id": "client456",
                "title": "Office Renovation",
                "status": "in_progress",
                "start_time": "2026-01-17T09:00:00",
                "end_time": "2026-01-17T17:00:00",
                "location": "123 Office St"
            }
        }


# ===== INVOICE MODELS =====

class LineItem(BaseModel):
    """Line item for an invoice"""
    description: str
    quantity: float
    rate: float
    amount: float

class InvoiceBase(BaseModel):
    """Base invoice model"""
    user_id: Optional[str] = None
    client_id: Optional[str] = None
    job_id: Optional[str] = None
    invoice_number: Optional[str] = None
    status: Optional[str] = "draft"  # draft, sent, paid, overdue, cancelled
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    line_items: Optional[List[LineItem]] = []
    total: Optional[float] = 0.0

class InvoiceCreate(InvoiceBase):
    """Model for creating a new invoice"""
    user_id: str  # Required
    client_id: str  # Required

class InvoiceUpdate(InvoiceBase):
    """Model for updating an invoice"""
    pass

class Invoice(InvoiceBase):
    """Complete invoice model with database fields"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "client_id": "client456",
                "job_id": "job789",
                "invoice_number": "INV-1001",
                "status": "sent",
                "issue_date": "2026-01-17",
                "due_date": "2026-02-16",
                "line_items": [
                    {
                        "description": "Labor - Office Renovation",
                        "quantity": 8,
                        "rate": 75.00,
                        "amount": 600.00
                    }
                ],
                "total": 600.00
            }
        }


# ===== RESPONSE MODELS =====

class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
