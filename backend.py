from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import supabase
import dotenv
import uvicorn
import os

EVENT = "Holi"

dotenv.load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to access the backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/get_user/{flat_number}")
async def get_user(flat_number: str):
    """Fetch user details based on flat number"""
    response = supabase_client.table("primaryData").select("*").eq("flatNumber", flat_number).execute()
    
    if not response.data or len(response.data) == 0:
        raise HTTPException(status_code=404, detail="Flat number not found")
    
    return response.data[0]  # Return first matching record

@app.post("/deduct_member/{flat_number}")
def deduct_member(flat_number: str):
    # Get user details
    response = supabase_client.table("primaryData").select("*").eq("flatNumber", flat_number).execute()
    data = response.data

    if not data:
        return {"error": "Flat number not found"}

    user = data[0]
    remaining_amount = user["remainingMembers"]

    if remaining_amount > 0:
        # Deduct 1 from remaining amount
        new_remaining = remaining_amount - 1
        supabase_client.table("primaryData").update({"remainingMembers": new_remaining}).eq("flatNumber", flat_number).execute()
        supabase_client.table("entryLogs").insert({"flatNumber": flat_number}).eq("event", EVENT).execute()
        return {"success": True, "message": "Member deducted", "remaining": new_remaining}
    else:
        return {"error": "No remaining members to deduct"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if no PORT is set
    uvicorn.run("backend:app", host="0.0.0.0", port=port, reload=True)