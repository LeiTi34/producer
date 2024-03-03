import os
import json

raw_api_configs = os.getenv("API_CONFIGS")
if not raw_api_configs:
    raise ValueError("API_CONFIGS environment variable is not set")

try:
    API_CONFIGS = json.loads(raw_api_configs)
except json.JSONDecodeError:
    raise ValueError("API_CONFIGS environment variable is not valid JSON")

if len(API_CONFIGS) == 0:
    raise ValueError("API_CONFIGS environment variable is empty")

for config in API_CONFIGS:
    if not isinstance(config, dict) or "URL" not in config or "TOPIC" not in config:
        raise ValueError("API_CONFIGS items must be dictionaries with 'URL' and 'TOPIC' keys")


KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
if not KAFKA_BROKER_URL:
    raise ValueError("KAFKA_BROKER_URL environment variable is not set")

