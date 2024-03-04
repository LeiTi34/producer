#!/bin/env python3

from kafka import KafkaProducer
import requests
import json
import math
from config.config import API_CONFIGS, KAFKA_BROKER_URL, KAFKA_TOPIC

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Failed to fetch data from {url}")
        return None

def publish_message(producer, topic, key, message):
    producer.send(topic, key=key.encode('utf-8'), value=message)
    producer.flush()

def fetch_and_publish_data(api_config, producer):
    page = 0
    total_pages = None

    while total_pages is None or page < total_pages:
        paginated_url = api_config["url"].replace("{PAGE}", str(page)).replace("{PAGE_SIZE}", str(api_config['page_size']))

        try:
            data = fetch_data(paginated_url)

            if total_pages is None and "total" in data:
                total_pages = math.ceil(data["total"] / api_config['page_size'])  # Ceiling division

            for product in data["results"]:
                product_id = product["productId"]
                publish_message(producer, KAFKA_TOPIC, f"{api_config['name']}-{product_id}", product)

        except requests.RequestException as e:
            print(f"Failed to fetch data from {paginated_url}: {e}")
            break 

        page += 1

def main():
    producer = KafkaProducer(
        bootstrap_servers = [KAFKA_BROKER_URL],
        value_serializer = lambda m: json.dumps(m).encode('utf-8')
    )

    for api_config in API_CONFIGS:
        fetch_and_publish_data(api_config, producer)

if __name__ == "__main__":
    main()
