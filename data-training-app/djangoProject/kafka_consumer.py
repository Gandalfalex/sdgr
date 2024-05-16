from kafka import KafkaConsumer
import numpy as np
import json
import time

# Create a Kafka consumer, subscribe to a specific topic and wait to get 100 elements,
# save the elements in a numpy array and break
consumer = KafkaConsumer(
    '702',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='my-group'
)
data = []

temp = {}

lastMessage = None

for message in consumer:
    print(message.value)
    
    #if len(data) == 100:
    #    print("finished")
    #    np_array = np.array(data)
    #    np.save(f'array_data.npy', np_array)
    #    break
    #else:
    #    print(len(data))
    #    data.append(float(message.value['value']))
    # Each message value is a list of numbers
    # We'll convert this list to a numpy array
    # np_array = np.array(message.value)

    # Save the numpy array to a file
    # We'll use the Kafka offset as the file name
    # np.save(f'array_{message.offset}.npy', np_array)
