import json
import zmq
import threading

# Function to create a new ZeroMQ socket for each thread
def create_socket():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.RCVTIMEO, 1000)  # Set a receive timeout of 1000 ms (1 second)
    return socket

# Function to generate a benign packet
def generate_benign_packet():
    return {
        "type": "benign",
        "data": "Normal traffic packet"
    }

# Function to simulate high traffic
def send_high_traffic(packet_count):
    socket = create_socket()  # Create a new socket for this thread
    for _ in range(packet_count):
        data = generate_benign_packet()  # Generate a benign packet
        print(f"Sending message: {data}")  # Log the message being sent
        socket.send(json.dumps(data).encode())  # Send the JSON-encoded data
        
        try:
            response = socket.recv().decode()  # Wait for a response
            print(f"Received response: {response}")  # Log the response received
        except zmq.Again:
            print("No response received in time.")  # Handle timeout case

# Main function to start the stress test
def main():
    total_packets_per_thread = 10  # Adjust this for the number of packets per thread
    num_threads = 10  # Number of concurrent threads

    # Create multiple threads to simulate concurrent traffic
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_high_traffic, args=(total_packets_per_thread,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
