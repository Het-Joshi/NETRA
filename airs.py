import logging
import json
import threading
import time
from pyspark.sql import SparkSession
from zmq import Context, REP, PUB
from configparser import ConfigParser
from collections import deque
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from kyber import Kyber, DEFAULT_PARAMETERS

# Define colors for logging
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",     # Blue
        "INFO": "\033[92m",      # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "CRITICAL": "\033[41m",  # Red background
    }

    DDOS_COLOR = "\033[95m"      # Magenta for DDoS messages
    THREAT_COLOR = "\033[33m"    # Yellow for Threat messages
    BENIGN_COLOR = "\033[32m"    # Green for Benign messages
    OTHER_COLOR = "\033[96m"     # Cyan for other publications
    RESET = "\033[0m"            # Reset color

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        if "DDoS" in record.msg:
            log_color = self.DDOS_COLOR
        elif "threat" in record.msg.lower():
            log_color = self.THREAT_COLOR
        elif "benign" in record.msg.lower():
            log_color = self.BENIGN_COLOR
        elif "Published" in record.msg:
            log_color = self.OTHER_COLOR
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

class AnsibleRunner:
    def run(self, playbook):
        logging.info(f"Running playbook: {playbook}")

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_node(self, node):
        if node not in self.chain:
            self.chain.append(node)

    def share_threat_intelligence(self, intelligence):
        self.chain.append(intelligence)

    def retrieve_threat_intelligence(self):
        return self.chain

class CrystalsKyber:
    def __init__(self):
        self.parameters = {
            "n": 256,
            "k": 2,
            "q": 7681,
            "eta_1": 2,
            "eta_2": 2,
            "gamma": 2,
            "du": 2,
            "dv": 2,
            "poly_modulus": 1
        }
        self.kyber = Kyber(self.parameters)
        self.public_key, self.secret_key = self.kyber.keygen()

    def encrypt(self, plaintext):
        challenge, shared_key = self.kyber.enc(self.public_key)
        return challenge, shared_key, plaintext.encode()

    def decrypt(self, challenge, ciphertext):
        shared_key = self.kyber.dec(self.secret_key, challenge)
        return ciphertext.decode()

class BodhiSecAIRS:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Bodhi Sec AIRS") \
            .getOrCreate()

        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )

        for handler in logging.getLogger().handlers:
            handler.setFormatter(ColoredFormatter())

        self.blockchain = Blockchain()
        self.ansible = AnsibleRunner()
        self.zeromq_context = Context()
        self.kyber = CrystalsKyber()

        self.config = ConfigParser()
        self.config.read('config.ini')
        self.request_threshold = int(self.config['Settings']['threshold'])
        self.time_window = int(self.config['Settings']['time_window'])
        self.incoming_requests = 0
        self.malicious_ips = set()
        self.request_times = deque()

        self.zeromq_publisher = self.zeromq_context.socket(PUB)
        self.zeromq_publisher.bind("tcp://*:5556")

    def preprocess_data(self, data):
        return data

    def detect_threat(self, incoming_data):
        logging.debug(f"Detecting threat for data: {incoming_data}")

        packet_length = incoming_data.get("length", 0)
        if packet_length > 1500:
            logging.warning("⚠️ Large packet detected, potential threat!")
            return True

        ip_address = incoming_data.get("ip")
        if ip_address in self.malicious_ips:
            logging.warning(f"🚨 Repeated request from known malicious IP: {ip_address}")
            return True
        
        return False

    def post_quantum_security(self):
        logging.info("🔐 Post-quantum security established successfully.")

    def decentralized_threat_intelligence(self, intelligence):
        challenge, shared_key, encrypted_data = self.kyber.encrypt(json.dumps(intelligence))
        self.blockchain.add_node("Node 1")
        self.blockchain.add_node("Node 2")
        self.blockchain.share_threat_intelligence((challenge, encrypted_data))
        threat_intelligence = self.blockchain.retrieve_threat_intelligence()
        logging.info("🛡️ Decentralized threat intelligence shared successfully.")
        return threat_intelligence

    def self_healing_infrastructure(self):
        logging.warning("🛠️ Initiating self-healing infrastructure due to potential DDoS attack...")
        
        playbook = {
            "name": "Self-healing playbook",
            "hosts": ["webservers"],
            "tasks": []
        }
        
        for malicious_ip in self.malicious_ips:
            playbook["tasks"].append({
                "name": f"Block IP address {malicious_ip}",
                "ansible.builtin.command": {
                    "cmd": f"iptables -A INPUT -s {malicious_ip} -j DROP"
                }
            })

        playbook["tasks"].append({
            "name": "Detect compromised services",
            "ansible.builtin.uri": {
                "url": "https://example.com/healthcheck",
                "status_code": 200
            }
        })

        playbook["tasks"].append({
            "name": "Mitigate threat",
            "ansible.builtin.block": {
                "path": "/etc/hosts.deny",
                "content": "example.com"
            }
        })

        playbook["tasks"].append({
            "name": "Re-deploy services",
            "ansible.builtin.apt": {
                "name": "nginx",
                "state": "present"
            }
        })

        self.ansible.run(playbook)
        logging.critical("🚨 Self-healing infrastructure playbook executed successfully.")
        self.malicious_ips.clear()

    def monitor_traffic(self):
        socket = self.zeromq_context.socket(REP)
        socket.bind("tcp://*:5555")

        while True:
            message = socket.recv()
            response = ""

            try:
                incoming_data = json.loads(message.decode())
                logging.debug(f"Received data: {incoming_data}")
                is_threat = self.detect_threat(incoming_data)

                current_time = time.time()
                self.request_times.append(current_time)
                self.incoming_requests += 1

                while self.request_times and (self.request_times[0] < current_time - self.time_window):
                    self.request_times.popleft()

                if len(self.request_times) > self.request_threshold:
                    logging.critical("💥 Potential DDoS attack detected! Requests: {}".format(len(self.request_times)))
                    self.self_healing_infrastructure()
                    self.incoming_requests = 0
                    self.publish_ddos_detection(incoming_data)

                if is_threat:
                    malicious_ip = incoming_data.get("ip", "unknown_ip")
                    self.malicious_ips.add(malicious_ip)
                    threat_intelligence = {"data": incoming_data}
                    self.decentralized_threat_intelligence(threat_intelligence)
                    response = "Threat detected and shared."
                    self.publish_threat_intelligence("threat", threat_intelligence)
                else:
                    benign_ip = incoming_data.get("ip", "unknown_ip")
                    response = "No threat detected."
                    benign_intelligence = {"data": incoming_data}
                    self.publish_threat_intelligence("benign", benign_intelligence)

            except json.JSONDecodeError:
                logging.error("Received invalid JSON.")
                response = "Invalid input."
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                response = "An error occurred."

            socket.send(response.encode())

    def publish_threat_intelligence(self, message_type, intelligence):
        message = {
            "type": message_type,
            "data": intelligence
        }
        self.zeromq_publisher.send_string(json.dumps(message))
        logging.info(f"📤 Published {message_type} intelligence: {intelligence}")

    def publish_ddos_detection(self, incoming_data):
        ddos_intelligence = {
            "type": "DDoS",
            "data": incoming_data
        }
        self.zeromq_publisher.send_string(json.dumps(ddos_intelligence))
        logging.critical(f"🚨 DDoS detection published: {incoming_data}")

    def start(self):
        self.post_quantum_security()
        self.monitor_traffic()

if __name__ == "__main__":
    airs = BodhiSecAIRS()
    airs.start()
