import os
from datetime import datetime, timezone
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

LOCK_TABLE = "user_locks"
LOCK_DURATION_SECONDS = 300

def is_user_locked(user_id: int) -> bool:
    try:
        response = supabase.table(LOCK_TABLE).select("locked_at").eq("user_id", user_id).single().execute()
        data = response.data
        if not data or "locked_at" not in data:
            return False
        locked_at_str = data["locked_at"]
        if locked_at_str.endswith("Z"):
            locked_at = datetime.fromisoformat(locked_at_str.replace("Z", "+00:00"))
        else:
            locked_at = datetime.fromisoformat(locked_at_str)
        if locked_at.tzinfo is None:
            locked_at = locked_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if (now - locked_at).total_seconds() < LOCK_DURATION_SECONDS:
            return True
        else:
            unlock_user(user_id)
            return False
    except Exception:
        return False

def lock_user(user_id: int, ex: int = LOCK_DURATION_SECONDS):
    now = datetime.now(timezone.utc).isoformat()
    try:
        supabase.table(LOCK_TABLE).upsert({"user_id": user_id, "locked_at": now}).execute()
    except Exception:
        pass

def unlock_user(user_id: int):
    try:
        supabase.table(LOCK_TABLE).delete().eq("user_id", user_id).execute()
    except Exception:
        pass