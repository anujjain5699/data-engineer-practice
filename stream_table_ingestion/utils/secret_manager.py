# ─────────────────────────────────────────────────────────────────────
#  PURPOSE: Single place to fetch all secrets via Databricks dbutils
#  WHY:     Keeps secret logic isolated — easy to swap later if needed
#

from databricks.sdk.runtime import dbutils       
from config.settings import (
    SECRET_SCOPE,
    SECRET_KEY_STORAGE_KEY,
    SECRET_KEY_ACCOUNT_NAME,
    SECRET_KEY_CONTAINER_NAME
)


def get_secret(key:str)->str:
    """
    fetch a single secret from databricks secret scope.
    secret scope is backed by azure key vault (adbease-kv).
    Args:
        key: the secret name/label as stored in key vault.
    
    Returns:
        str: the secret value
    """
    try:
        return dbutils.secrets.get(scope=SECRET_SCOPE, key= key)
    except Exception as e:
        raise RuntimeError(
            f"❌ Failed to fetch secret '{key}' from scope '{SECRET_SCOPE}'.\n"
            f"   Check: Secret Scope exists | Secret name is correct | You have permission.\n"
            f"   Error: {e}"
        )

def get_all_secrets() -> dict:
    """
    Fetches all required ADLS secrets in one call.

    Returns:
        dict with keys: storage_key, account_name, container_name
    """
    print("🔑 Fetching secrets from Databricks Secret Scope...")

    secrets = {
        "storage_key":    get_secret(SECRET_KEY_STORAGE_KEY),
        "account_name":   get_secret(SECRET_KEY_ACCOUNT_NAME),
        "container_name": get_secret(SECRET_KEY_CONTAINER_NAME)
    }

    print(f"   ✅ adls-storage-key     → [REDACTED]")
    print(f"   ✅ adls-account-name    → [REDACTED]")
    print(f"   ✅ adls-container-name  → [REDACTED]")
    print("   ✅ All secrets loaded securely!\n")

    return secrets
