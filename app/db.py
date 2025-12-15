import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = None

try:
    if not url or not key:
        raise ValueError("Supabase credentials missing")

    supabase = create_client(url, key)

    #  REAL CONNECTION TEST
    supabase.table("sessions").select("*").limit(1).execute()

    print("Supabase connected successfully")

except Exception as e:
    supabase = None
    print("Supabase connection failed:", e)
