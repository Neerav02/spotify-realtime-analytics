import pandas as pd
from kafka import KafkaProducer
import json, time, os

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Corrected filename from your 'ls' command
csv_path = r"D:\BDA\spotify_project\data\Spotify_2024_Global_Streaming_Data.csv"

def stream_data():
    if not os.path.exists(csv_path):
        print(f"!!! File NOT found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    print("--- Starting Stream ---")
    for i, row in df.iterrows():
        payload = {
            "genre": str(row['Genre']),
            "streams": float(row['Total Streams (Millions)']),
            "skip_rate": float(row['Skip Rate (%)'])
        }
        producer.send('spotify_topic', payload)
        print(f"Sent Batch {i}: {payload['genre']}")
        time.sleep(1)

if __name__ == "__main__":
    stream_data()