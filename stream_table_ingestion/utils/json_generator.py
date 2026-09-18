# filename: utils/json_generator.py
# ─────────────────────────────────────────────────────────────────────
#  PURPOSE: Generates sample order JSON data and saves locally
#  WHY:     Data generation logic stays separate and is easily reusable
# ──

import json
import uuid
from datetime import datetime, timezone


def generate_orders(num_records: int = 3) -> list:
    """
    Generates a list of sample order records.
    Simulates data from an Order Management System (OMS).

    Args:
        num_records: Number of order records to generate

    Returns:
        List of order dictionaries
    """
    channels  = ["online", "in-store", "mobile-app"]
    statuses  = ["confirmed", "processing", "shipped"]
    store_ids = ["STORE-NYC-05", "STORE-LA-02", "STORE-CHI-03"]

    return [
        {
            "order_id":      f"ORD-{uuid.uuid4().hex[:8].upper()}",
            "customer_id":   f"CUST-{1000 + i}",
            "customer_name": f"Customer {1000 + i}",
            "order_date":    datetime.now(timezone.utc).isoformat(),
            "store_id":      store_ids[i % len(store_ids)],
            "channel":       channels[i % len(channels)],
            "status":        statuses[i % len(statuses)],
            "currency":      "USD",
            "total_amount":  round(49.99 + (i * 25.50), 2),
            "items": [
                {
                    "sku":        f"SKU-{i:04d}",
                    "name":       f"Product {i}",
                    "qty":        1,
                    "unit_price": round(49.99 + (i * 25.50), 2)
                }
            ],
            "shipping_address": {
                "city":  "New York",
                "state": "NY",
                "zip":   "10001"
            }
        }
        for i in range(num_records)
    ]


def save_orders_json(file_path: str, num_records: int = 3) -> None:
    """
    Generates orders and saves them as a JSON file locally.

    Args:
        file_path:   Local path to save the file (/tmp/... in Databricks)
        num_records: Number of order records to generate
    """
    orders = generate_orders(num_records)

    with open(file_path, "w") as f:
        json.dump(orders, f, indent=2)

    print(f"📄 JSON file created: {file_path} ({len(orders)} records)")