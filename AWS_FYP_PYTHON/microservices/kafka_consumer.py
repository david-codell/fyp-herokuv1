from confluent_kafka import Consumer, KafkaError

# Configure the Kafka consumer
conf = {
    'bootstrap.servers': '127.0.0.1:9092',  # Replace with your Kafka broker address
    'group.id': 'user-processing-group',           # Replace with your consumer group ID
    'auto.offset.reset': 'earliest'             # Adjust the offset reset strategy as needed
}

# Create a Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to a Kafka topic
consumer.subscribe(['register'])  # Replace with the topic you want to consume from

try:
    while True:
        # Poll for messages
        msg = consumer.poll(1.0)  # Adjust the timeout as needed

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Reached end of partition {msg.partition()}")
            else:
                print(f"Error while consuming message: {msg.error()}")
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass

finally:
    # Close the Kafka consumer
    consumer.close()
