# db/supabase_client.py
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# No data transformation or model construction is present here, but add a comment for future maintainers.
# If you add any data transformation or model construction here, ensure to add Pydantic validation and error handling.
