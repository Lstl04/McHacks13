from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from ..models import Invoice, InvoiceCreate, InvoiceUpdate, MessageResponse
from ..database import get_database

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice(invoice: InvoiceCreate):
    """Create a new invoice"""
    db = get_database()
    
    # Validate IDs
    if not ObjectId.is_valid(invoice.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    if not ObjectId.is_valid(invoice.client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    
    # Auto-generate invoice number if not provided
    if not invoice.invoice_number:
        # Get user's last invoice number
        user = db.users.find_one({"_id": ObjectId(invoice.user_id)})
        if user:
            last_number = user.get("lastInvoiceNumber", 1000)
            invoice.invoice_number = f"INV-{last_number + 1}"
            
            # Update user's last invoice number
            db.users.update_one(
                {"_id": ObjectId(invoice.user_id)},
                {"$set": {"lastInvoiceNumber": last_number + 1}}
            )
    
    # Insert invoice
    invoice_dict = invoice.model_dump(exclude_unset=True)
    result = db.invoices.insert_one(invoice_dict)
    
    # Return created invoice
    created_invoice = db.invoices.find_one({"_id": result.inserted_id})
    return created_invoice

@router.get("/", response_model=List[Invoice])
async def get_invoices(
    user_id: str = None,
    client_id: str = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """Get all invoices with optional filters"""
    db = get_database()
    
    query = {}
    if user_id:
        query["user_id"] = user_id
    if client_id:
        query["client_id"] = client_id
    if status_filter:
        query["status"] = status_filter
    
    invoices = list(db.invoices.find(query).skip(skip).limit(limit))
    return invoices

@router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: str):
    """Get a specific invoice by ID"""
    db = get_database()
    
    if not ObjectId.is_valid(invoice_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
    invoice = db.invoices.find_one({"_id": ObjectId(invoice_id)})
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    return invoice

@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: str, invoice_update: InvoiceUpdate):
    """Update an invoice"""
    db = get_database()
    
    if not ObjectId.is_valid(invoice_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
    update_data = invoice_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = db.invoices.update_one(
        {"_id": ObjectId(invoice_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    updated_invoice = db.invoices.find_one({"_id": ObjectId(invoice_id)})
    return updated_invoice

@router.delete("/{invoice_id}", response_model=MessageResponse)
async def delete_invoice(invoice_id: str):
    """Delete an invoice"""
    db = get_database()
    
    if not ObjectId.is_valid(invoice_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
    result = db.invoices.delete_one({"_id": ObjectId(invoice_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    return {"message": f"Invoice {invoice_id} deleted successfully"}
