import json
import zmq
import random
import time

# Initialize ZeroMQ context and request socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Function to generate a malicious packet
def generate_malicious_packet():
    packet_length = random.randint(1000, 2000)  # Simulating large packet lengths
    return {
        "type": "malicious",
        "length": packet_length,
        "payload": "Malicious payload: " + ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=packet_length))
    }

# Function to generate a benign packet
def generate_benign_packet():
    packet_length = random.randint(50, 500)  # Simulating normal packet lengths
    return {
        "type": "benign",
        "length": packet_length,
        "payload": "Benign payload: Normal data packet"
    }

while True:
    # Randomly choose to send either a malicious or benign packet
    if random.random() < 0.5:
        data = generate_malicious_packet()  # Generate a malicious packet
    else:
        data = generate_benign_packet()  # Generate a benign packet

    print(f"Sending message: {data}")  # Log the message being sent
    socket.send(json.dumps(data).encode())  # Send the JSON-encoded data
    response = socket.recv().decode()  # Wait for a response
    print(f"Received response: {response}")  # Log the response received
    time.sleep(random.uniform(0.1, 1))  # Simulate varying traffic rates
