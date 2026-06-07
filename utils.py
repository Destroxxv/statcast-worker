import hmac
import hashlib
import json
from config import STATCAST_WEBHOOK_SECRET

def sign_payload(payload: dict) -> str:
    message = json.dumps(payload, sort_keys=True).encode()
    secret = STATCAST_WEBHOOK_SECRET.encode()

    return hmac.new(secret, message, hashlib.sha256).hexdigest()
