from typing import Dict, List, Tuple
from core.config import get_secret
def get_provider_secrets(required_keys: List[str]) -> Tuple[Dict[str, str], List[str]]:
    cfg = {}; missing = []
    for k in required_keys:
        v = get_secret(k, "")
        if not v: missing.append(k)
        cfg[k] = v
    return cfg, missing
