import argparse
import requests
import math
import json
from itertools import chain
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from config import API_CONFIGS, KAFKA_BROKER_URL, KAFKA_TOPIC, SCHEMA_REGISTRY_URL

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Failed to fetch data from {url}")
        return None

def save_messages(messages, filename="saved_messages.json"):
    with open(filename, "w") as f:
        json.dump(messages, f)

def read_messages(filename="saved_messages.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Saved messages file not found.")
        return []

def main(mode):
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    with open("src/products.avsc", "r") as schema_file:
        product_avro_schema = json.load(schema_file)

    avro_serializer = AvroSerializer(schema_str=json.dumps(product_avro_schema),
                                     schema_registry_client=schema_registry_client)

    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER_URL,
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': avro_serializer,
    }

    producer = SerializingProducer(producer_conf)

    if mode == 'read':
        messages = read_messages()
        for msg in messages:
            publish_message(producer, KAFKA_TOPIC, msg["key"], msg["message"])
    else:
        messages = []
        for api_config in API_CONFIGS:
            fetched_messages = fetch_and_publish_data(api_config, producer, mode == 'save')
            messages.extend(fetched_messages)

        if mode == 'save':
            save_messages(messages)

def fetch_and_publish_data(api_config, producer, save=False):
    page = 0
    total_pages = None
    messages = []

    while total_pages is None or page < total_pages:
        paginated_url = api_config["url"].replace("{PAGE}", str(page)).replace("{PAGE_SIZE}", str(api_config['page_size']))

        try:
            data = fetch_data(paginated_url)

            if total_pages is None and "total" in data:
                total_pages = math.ceil(data["total"] / api_config['page_size'])

            if data is None:
                break

            for product in data["results"]:
                product_id = product["productId"]
                flattened_categories = list(chain.from_iterable(product['parentCategories']))
                product['parentCategories'] = flattened_categories

                if save:
                    messages.append({"key": f"{api_config['name']}-{product_id}", "message": product})
                else:
                    publish_message(producer, KAFKA_TOPIC, f"{api_config['name']}-{product_id}", product)

        except requests.RequestException as e:
            print(f"Failed to fetch data from {paginated_url}: {e}")
            break

        page += 1

    return messages

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
    parser = argparse.ArgumentParser(description='Process input arguments for different modes.')
    parser.add_argument('--save', action='store_true', help='Save the messages in a JSON file')
    parser.add_argument('--read', action='store_true', help='Read from the saved JSON file and publish to Kafka')

    args = parser.parse_args()

    if args.save:
        main_mode = 'save'
    elif args.read:
        main_mode = 'read'
    else:
        main_mode = None

    main(main_mode)
