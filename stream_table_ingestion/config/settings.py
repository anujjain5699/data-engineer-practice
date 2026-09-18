# ── Databricks Secret Scope ───────────────────────────────────────────
# Name of the Secret Scope you created via #secrets/createScope URL
SECRET_SCOPE = "easewithdata-storage-scope"

SECRET_KEY_STORAGE_KEY    = "adbease-storage-key" 
SECRET_KEY_ACCOUNT_NAME   = "adbease-account-name"   
SECRET_KEY_CONTAINER_NAME = "adbease-container-name"

# ── ADLS Path Config ─────────────────────────────────────────────────
UPLOAD_FOLDER   = "incoming/orders"                 # folder path in container
LOCAL_FILE_PATH = "/tmp/orders_batch.json"          # temp path in Databricks

# ── Streaming Table Config ────────────────────────────────────────────
STREAMING_TABLE_NAME = "orders_bronze"
STREAMING_TABLE_COMMENT = "Bronze: raw orders ingested from ADLS Gen2"
