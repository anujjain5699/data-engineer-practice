# filename: utils/adls_client.py
# ─────────────────────────────────────────────────────────────────────
#  PURPOSE: Handles all ADLS Gen2 connection and file upload logic
#  WHY:     Storage logic stays separate from business logic
# 
from datetime import datetime, timezone
from azure.storage.filedatalake import DataLakeServiceClient
from config.settings import UPLOAD_FOLDER

def get_adls_client(account_name: str, account_key: str) -> DataLakeServiceClient:
    """
    Creates and returns an authenticated ADLS Gen2 service client.

    Args:
        account_name: Storage account name (from Key Vault)
        account_key:  Storage account key  (from Key Vault)

    Returns:
        Authenticated DataLakeServiceClient
    """
    try:
        client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=account_key
        )
        print(f"☁️  Connected to ADLS Gen2: {account_name}")
        return client
    except Exception as e:
        raise RuntimeError(
            f"❌ Failed to connect to ADLS Gen2 account '{account_name}'.\n"
            f"   Check your storage key and account name.\n"
            f"   Error: {e}"
        )


def upload_file(
    client: DataLakeServiceClient,
    container_name: str,
    local_file_path: str
) -> str:
    """
    Uploads a local file to ADLS Gen2 with a timestamped filename.

    Args:
        client:          Authenticated DataLakeServiceClient
        container_name:  Target container (e.g. raw-data)
        local_file_path: Path to local file on Databricks driver (/tmp/...)

    Returns:
        Full ABFSS path of the uploaded file (for Databricks streaming)
    """
    try:
        # Timestamped filename → prevents overwriting previous batches
        timestamp   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        upload_path = f"{UPLOAD_FOLDER}/orders_batch_{timestamp}.json"

        fs_client   = client.get_file_system_client(container_name)
        file_client = fs_client.get_file_client(upload_path)

        with open(local_file_path, "rb") as f:
            file_client.upload_data(f.read(), overwrite=True)

        account_name = client.account_name
        full_path = (
            f"abfss://{container_name}"
            f"@{account_name}.dfs.core.windows.net"
            f"/{UPLOAD_FOLDER}/"
        )

        print(f"🚀 File uploaded: {upload_path}")
        return full_path

    except Exception as e:
        raise RuntimeError(
            f"❌ Upload failed.\n"
            f"   Check container name and file path.\n"
            f"   Error: {e}"
        )