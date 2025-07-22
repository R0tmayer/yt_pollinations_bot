import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def is_user_allowed(username: str) -> bool:
    try:
        response = supabase.table("users").select("id").eq("username", username).execute()
        return bool(getattr(response, "data", None))
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
