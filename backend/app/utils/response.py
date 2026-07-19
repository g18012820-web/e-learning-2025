from datetime import datetime
from typing import Any, Dict, Optional


def standard_response(success: bool, message: str = "", data: Any = None, errors: Optional[Any] = None, meta: Optional[Dict] = None) -> Dict:
    if meta is None:
        meta = {"request_id": None, "timestamp": datetime.utcnow().isoformat() + 'Z'}
    return {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
        "meta": meta,
    }
