#!/bin/env python3

from kafka import KafkaProducer
import requests
import json
import math
from config.config import API_CONFIGS, KAFKA_BROKER_URL

PAGE_SIZE = 200

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Failed to fetch data from {url}")
        return None

def publish_message(producer, topic, message):
    if message is not None:
        producer.send(topic, value=message)
        producer.flush()

def fetch_and_publish_data(api_config, producer):
    page = 0
    total_pages = None

    while total_pages is None or page < total_pages:
        paginated_url = api_config["URL"].replace("{PAGE}", str(page)).replace("{PAGE_SIZE}", str(PAGE_SIZE))
        # print(paginated_url)

        try:
            data = fetch_data(paginated_url)

            if total_pages is None and "total" in data:
                total_pages = math.ceil(data["total"] / PAGE_SIZE)  # Ceiling division

            # print(f"{page + 1} / {total_pages}, {PAGE_SIZE * (page + 1)} / {data['total']}")
            data["current_page"] = page + 1
            data["total_pages"] = total_pages
            publish_message(producer, api_config["TOPIC"], data)

        except requests.RequestException as e:
            print(f"Failed to fetch data from {paginated_url}: {e}")
            break 

        page += 1

def main():
    producer = KafkaProducer(
        bootstrap_servers = [KAFKA_BROKER_URL],
        value_serializer = lambda m: json.dumps(m).encode('utf-8')
    )

    for api in API_CONFIGS:
        fetch_and_publish_data(api, producer)

if __name__ == "__main__":
    main()
