# Technical Indicator Service

This service ingests candle data from a Kafka candle topic, computes various technical indicators using the TA-Lib Python library, and pushes the results back to Kafka.

## Prerequisites

Before running the technical indicator service, ensure the following prerequisites are met:

1. **Redpanda Dev Cluster**: Power up the Redpanda dev cluster.
2. **Trades and Candles Services**: Ensure the trades and candles services are running. These services help compute the technical indicators in real-time by providing the necessary data.

## Setup Instructions

 1. Switch to the Service Folder

    Navigate to the technical indicators service directory:

```sh
cd services/technical-indicators/
```
 2. Install ta-lib library dependencies in linux (it's an additional dependcy)
 ```sh
sudo apt-get update
sudo apt-get install -y build-essential wget
```

```sh
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
```

 3. Sync the python dependencies for service using UV.
 ```python
 uv sync --frozen
 ```

 4. All set, run service..( install make and turn on Docker or Docker Desktop before running below command)
 ```sh
 uv run python run.py  
 or 
 make run
```
