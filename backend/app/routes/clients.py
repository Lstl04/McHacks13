from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from ..models import Client, ClientCreate, ClientUpdate, MessageResponse
from ..database import get_database

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate):
    """Create a new client"""
    db = get_database()
    
    # Verify user exists
    if not ObjectId.is_valid(client.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Insert client
    client_dict = client.model_dump(exclude_unset=True)
    result = db.clients.insert_one(client_dict)
    
    # Return created client
    created_client = db.clients.find_one({"_id": result.inserted_id})
    return created_client

@router.get("/", response_model=List[Client])
async def get_clients(user_id: str = None, skip: int = 0, limit: int = 100):
    """Get all clients, optionally filtered by user_id"""
    db = get_database()
    
    query = {}
    if user_id:
        query["user_id"] = user_id
    
    clients = list(db.clients.find(query).skip(skip).limit(limit))
    return clients

@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: str):
    """Get a specific client by ID"""
    db = get_database()
    
    if not ObjectId.is_valid(client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    
    client = db.clients.find_one({"_id": ObjectId(client_id)})
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    return client

@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client_update: ClientUpdate):
    """Update a client"""
    db = get_database()
    
    if not ObjectId.is_valid(client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    
    update_data = client_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = db.clients.update_one(
        {"_id": ObjectId(client_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    updated_client = db.clients.find_one({"_id": ObjectId(client_id)})
    return updated_client

@router.delete("/{client_id}", response_model=MessageResponse)
async def delete_client(client_id: str):
    """Delete a client"""
    db = get_database()
    
    if not ObjectId.is_valid(client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    
    result = db.clients.delete_one({"_id": ObjectId(client_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    return {"message": f"Client {client_id} deleted successfully"}
