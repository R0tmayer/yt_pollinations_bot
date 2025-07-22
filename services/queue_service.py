import os
from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

LOCK_TIMEOUT = 300

def is_user_locked(username: str) -> bool:
    now = datetime.now(timezone.utc)
    resp = supabase.table("user_locks").select("*").eq("username", username).execute()
    if resp.data:
        locked_at_str = resp.data[0]["locked_at"]
        is_locked = resp.data[0].get("IsLocked", False)
        if not is_locked:
            return False
        if locked_at_str.endswith("Z"):
            locked_at = datetime.fromisoformat(locked_at_str.replace("Z", "+00:00"))
        else:
            locked_at = datetime.fromisoformat(locked_at_str)
        if locked_at.tzinfo is None:
            locked_at = locked_at.replace(tzinfo=timezone.utc)
        if (now - locked_at).total_seconds() < LOCK_TIMEOUT:
            return True
    return False

def lock_user(username: str):
    print(f"Блокирую пользователя {username}")
    now = datetime.now(timezone.utc).isoformat()
    supabase.table("user_locks").upsert({"username": username, "locked_at": now, "IsLocked": True}).execute()

def unlock_user(username: str):
    supabase.table("user_locks").update({"IsLocked": False}).eq("username", username).execute()