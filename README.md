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

Then load the config environment:

```bash
source env.sh
```

### Windows

Use WSL?

## Config

Configuration is done with environment variables (see `env.sh` for default config).

The following variables are expected:

| Variable           | Description                                            | Example                                                  |
| ------------------ | ------------------------------------------------------ | -------------------------------------------------------- |
| `KAFKA_BROKER_URL` | Connection to kafka broker                             | `localhost:29092`                                        |
| `API_CONFIGS`      | JSON array of API configurations (URL and kafka topic) | `[{"URL": "https://api.example.com", "TOPIC": "api-1"}]` |

## Running

Execute the script with:

```bash
python3 src/main.py
```

