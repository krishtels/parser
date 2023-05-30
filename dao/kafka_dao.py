from json import dumps, loads

from kafka import KafkaConsumer, KafkaProducer


class KafkaSetup:
    def __init__(self):
        self.producer = KafkaProducer(
            retries=1,
            bootstrap_servers=["kafka:9092"],
            value_serializer=lambda x: dumps(x).encode("utf-8"),
            api_version=(0, 10, 1),
        )
        self.consumer_lamoda = KafkaConsumer(
            "lamoda",
            bootstrap_servers=["kafka:9092"],
            auto_offset_reset="earliest",
            consumer_timeout_ms=5000,
            group_id="1",
            api_version=(0, 10, 1),
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )
        self.consumer_twitch = KafkaConsumer(
            "twitch",
            bootstrap_servers=["kafka:9092"],
            auto_offset_reset="earliest",
            consumer_timeout_ms=5000,
            group_id="2",
            api_version=(0, 10, 1),
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )
        self.consumer_lamoda.subscribe(topics=["lamoda"])
        self.consumer_twitch.subscribe(topics=["twitch"])
