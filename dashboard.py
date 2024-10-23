import streamlit as st
import json
import zmq
import time
import pandas as pd
from collections import deque

# Set up ZeroMQ to receive real-time data from the AIRS system
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")  # Connect to the PUB socket
socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe to all messages

# Initialize packet counters
benign_count = 0
malicious_count = 0

# Store recent requests for display (max 10 recent requests)
recent_requests = deque(maxlen=10)

# Initialize lists for graph data
benign_packet_history = []
malicious_packet_history = []
time_history = []

# Streamlit dashboard layout
st.set_page_config(page_title="AIRS Dashboard", layout="wide")
st.title("Automated Incident Response System (AIRS)")

# Metrics
st.subheader("System Metrics")
col1, col2 = st.columns(2)
with col1:
    benign_counter = st.empty()
with col2:
    malicious_counter = st.empty()

# Threat Intelligence Log
st.subheader("Threat Intelligence Sharing")
threat_log = st.empty()

# Real-Time Threat Detection
st.subheader("Threat Detection")
threat_detected = st.empty()

# Self-Healing Status
st.subheader("Self-Healing Infrastructure")
self_healing_status = st.empty()

# Graph section for packet counts over time
st.subheader("Packet Count Over Time")
graph_placeholder = st.empty()

# Function to process incoming messages
def process_message(message):
    global benign_count, malicious_count, recent_requests, benign_packet_history, malicious_packet_history, time_history

    try:
        # Parse the incoming message
        data = json.loads(message)
        msg_type = data.get("type", "Unknown")
        msg_data = data.get("data", {})

        # Update counters and threat detection based on message type
        if msg_type == "threat":
            malicious_count += 1  # Increment malicious packet count
            threat_detected.warning(f"Threat detected from IP: {msg_data.get('ip', 'unknown')}")
            recent_requests.append(msg_data)
        elif msg_type == "benign":
            benign_count += 1  # Increment benign packet count
            threat_detected.success(f"No threat detected from IP: {msg_data.get('ip', 'unknown')}")
            recent_requests.append(msg_data)

        # Show threat intelligence shared in the blockchain
        threat_log.json(msg_data)

        # Update packet counters
        benign_counter.metric("Benign Packets", benign_count)
        malicious_counter.metric("Malicious Packets", malicious_count)

        # Update time and packet histories for the graph
        current_time = time.strftime("%H:%M:%S")  # Get current time as a string
        time_history.append(current_time)
        benign_packet_history.append(benign_count)
        malicious_packet_history.append(malicious_count)

        # Keep history size manageable (max 20 points for the graph)
        if len(time_history) > 20:
            time_history.pop(0)
            benign_packet_history.pop(0)
            malicious_packet_history.pop(0)

        # Create a DataFrame for the graph
        df = pd.DataFrame({
            "Time": time_history,
            "Benign Packets": benign_packet_history,
            "Malicious Packets": malicious_packet_history
        })

        # Set "Time" as the index
        df = df.set_index("Time")

        # Update the graph with the new data
        graph_placeholder.line_chart(df)

    except json.JSONDecodeError:
        st.error("Received invalid data format.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Stream data and update the dashboard in real time
while True:
    try:
        # Attempt to receive a message from ZeroMQ
        message = socket.recv_string(flags=zmq.NOBLOCK)
        process_message(message)
    except zmq.Again:
        # No message received, continue loop
        pass
    time.sleep(1)  # Throttle to prevent excessive CPU usage
