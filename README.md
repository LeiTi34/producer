# Bier in Aktion Producer

## Setup

### Nix

Just run `nix-shell`.

### Linux

Create a python virtual environment and install the requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install [`protoc`](https://protobuf.dev/downloads/) and generate the Protobuf classes:

```bash
./generate_classes.sh
```

Then load the config environment:

```bash
source env.sh
```

### Windows

Use WSL2?

## Config

Configuration is done with environment variables (see `env.sh` for default config).

The following variables are expected:

| Variable              | Description                                                       | Example                                                                   |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `KAFKA_BROKER_URL`    | Connection to Kafka broker                                        | `localhost:29092`                                                         |
| `KAFKA_TOPIC`         | Kafka topic name                                                  | `products`                                                                |
| `API_CONFIGS`         | JSON array of API configurations (URL, page size and Kafka topic) | `[{"url": "https://api.example.com", "name": "api-1", "page_size": 10 }]` |
| `SCHEMA_REGISTRY_URL` | URL to the schema registry                                        | `http://localhost:8081`                                                   |

## Running

Execute the script with:

```bash
python3 src/main.py
```

