from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from config.config import API_CONFIGS, KAFKA_BROKER_URL, KAFKA_TOPIC, SCHEMA_REGISTRY_URL
import requests
import math
from protobuf.generated_classes.product_pb2 import Product
from google.protobuf.json_format import ParseDict
from itertools import chain


def main():
    schema_registry_conf = {
        'url': SCHEMA_REGISTRY_URL,
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    serializer_conf = {
        'use.deprecated.format': False,
    }
    protobuf_serializer = ProtobufSerializer(Product, schema_registry_client, serializer_conf)

    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER_URL,
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': protobuf_serializer,
    }
    producer = SerializingProducer(producer_conf)

    for api_config in API_CONFIGS:
        fetch_and_publish_data(api_config, producer)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Failed to fetch data from {url}")
        return None

def fetch_and_publish_data(api_config, producer):
    page = 0
    total_pages = None

    while total_pages is None or page < total_pages:
        paginated_url = api_config["url"].replace("{PAGE}", str(page)).replace("{PAGE_SIZE}", str(api_config['page_size']))

        try:
            data = fetch_data(paginated_url)

            if total_pages is None and "total" in data:
                total_pages = math.ceil(data["total"] / api_config['page_size'])  # Ceiling division

            if data is None:
                break

            for product in data["results"]:
                product_id = product["productId"]
                flattened_categories = list(chain.from_iterable(map(lambda x: x, product['parentCategories'])))
                product['parentCategories'] = flattened_categories
                parsed_product = ParseDict(product, Product())
                publish_message(producer, KAFKA_TOPIC, f"{api_config['name']}-{product_id}", parsed_product)

        except requests.RequestException as e:
            print(f"Failed to fetch data from {paginated_url}: {e}")
            break 

        page += 1

def publish_message(producer, topic, key, message):
    print("publishing message")
    producer.produce(topic=topic, key=key, value=message, on_delivery=delivery_report)
    producer.poll(0)
    producer.flush()

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    main()

