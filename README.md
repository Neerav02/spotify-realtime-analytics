## 🎵 Spotify Real-Time Analytics 
PipelineAn end-to-end Big Data pipeline that ingests, processes, and visualizes Spotify streaming trends in real-time using Apache Kafka, PySpark, PostgreSQL, and Grafana.

## 🚀 Project Overview
This project addresses the challenge of processing high-volume streaming data to derive actionable insights. By simulating a live stream of global music data, the system calculates popularity and engagement metrics (skip rates) on the fly, allowing for immediate visualization of listener behavior.Key Features:Real-Time Ingestion: Python producer streaming JSON-serialized music data to Kafka.Distributed Processing: PySpark Structured Streaming for live aggregations.Relational Storage: Processed metrics stored in a Dockerized PostgreSQL database.Dynamic Dashboarding: Live Grafana panels showing genre popularity and skip-rate thresholds.🛠 Tech StackLanguage: Python 3.10+ (via .venv)Stream Broker: Apache Kafka (Confluent Platform)Processing Engine: Apache Spark 3.5.0Database: PostgreSQL 13Containerization: Docker & Docker ComposeVisualization: Grafana

## 📂 Project Structure

spotify_project/
├── data/               # Source Dataset (Spotify_2024_Global_Streaming_Data.csv)
├── hadoop/             # Windows Hadoop binaries (winutils.exe, hadoop.dll)
├── scripts/
│   ├── producer.py     # Kafka Ingestion Script
│   └── processor.py    # Spark Streaming Script
├── docker-compose.yml  # Microservices Configuration
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation

## ⚙️ Setup & Installation

1. Environment Setup
Activate your local virtual environment and install dependencies:
PowerShellpython -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

2. Launch Infrastructure
Start the Kafka broker and PostgreSQL database using Docker:
PowerShelldocker-compose up -d

3. Initialize Database
Connect to the database and create the analytics table:
SQLCREATE TABLE spotify_stats (
    genre VARCHAR(100) PRIMARY KEY,
    avg_skip FLOAT,
    total_streams FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## 🏃 Execution Flow
Step              Command                          Description
1. Producer       python scripts/producer.py       Reads CSV and pushes data to Kafka.
2. Processor      python scripts/processor.py      Spark consumes Kafka topic and writes to Postgres.
3. Visualize      localhost:3000                   Open Grafana to view the live dashboard.

## 🔮 Future Enhancements
Predictive Analytics: Integrate a Python-based ML model to predict future genre trends.

Sentiment Analysis: Connect a Natural Language Processing (NLP) layer to analyze track titles or metadata.

Cloud Deployment: Transition the Docker environment to AWS or Azure for global scalability.

Complex Event Processing (CEP): Implement window-based alerts for sudden spikes in genre popularity.

## 🤝 Troubleshooting Notes
During development, we resolved several critical environment issues:

Hadoop Pathing: Fixed winutils.exe requirements for local Spark instances on Windows.

JDBC Authentication: Resolved PostgreSQL authentication failures by synchronizing Spark driver credentials.

Kafka Serialization: Implemented JSON encoding for seamless data transfer between the producer and Spark.

## 👤 Author
* **Neerav Babel**
* **LinkedIn**: https://www.linkedin.com/in/neerav-babel-2b3a7a226?utm_source=share_via&utm_content=profile&utm_medium=member_android
* **GitHub**: https://github.com/Neerav02
