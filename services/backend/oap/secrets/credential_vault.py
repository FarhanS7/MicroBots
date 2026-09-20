import base64
from typing import Dict
from pydantic import BaseModel, Field

class F08Input(BaseModel):
    provider: str = Field(..., description="Target model or service provider")
    credential: str = Field(..., description="Raw provider API credential/key")

class F08Output(BaseModel):
    secret_id: str
    configured: bool

class ForbiddenSecretError(Exception):
    """Raised when attempting to resolve a revoked or forbidden secret handle."""
    def __init__(self, message: str = "Access to revoked credential handle is forbidden") -> None:
        self.message = message
        super().__init__(message)

# In-memory vault store for credentials
_VAULT: Dict[str, Dict[str, str | bool]] = {}

def credential_vault(input_data: F08Input, secret_id: str = "secret-1") -> F08Output:
    """
    Encrypts (base64 mock) and stores provider credential behind a secret_id handle.
    """
    encrypted = base64.b64encode(input_data.credential.encode("utf-8")).decode("utf-8")
    _VAULT[secret_id] = {
        "provider": input_data.provider,
        "encrypted_credential": encrypted,
        "revoked": False,
    }
    return F08Output(secret_id=secret_id, configured=True)

def resolve_credential(secret_id: str) -> str:
    """
    Resolves secret handle to decrypted credential at authorized provider boundary.
    """
    record = _VAULT.get(secret_id)
    if not record or record.get("revoked"):
        raise ForbiddenSecretError("Access to revoked credential handle is forbidden")
    
    enc_val = str(record["encrypted_credential"])
    return base64.b64decode(enc_val.encode("utf-8")).decode("utf-8")

def revoke_credential(secret_id: str) -> None:
    """
    Revokes a credential handle.
    """
    if secret_id in _VAULT:
        _VAULT[secret_id]["revoked"] = True

def reset_vault() -> None:
    _VAULT.clear()
