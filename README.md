# NETRA: Automated Incident Response System (AIRS)

NETRA is an Automated Incident Response System (AIRS) designed to enhance cybersecurity through advanced threat detection, decentralized threat intelligence sharing, and self-healing infrastructure. Leveraging cutting-edge technologies such as ZeroMQ, PySpark, and post-quantum cryptography, Bodhi-Sec provides a robust framework to mitigate cyber threats in real time.

## Features

- **Threat Detection**: Monitors incoming network traffic for potential threats, including DDoS attacks and other malicious activities.
- **Decentralized Threat Intelligence**: Shares threat intelligence securely across a blockchain-like structure, enhancing collaborative defense mechanisms.
- **Self-Healing Infrastructure**: Automatically blocks malicious IPs and redeploys services to maintain operational continuity during attacks.
- **Post-Quantum Security**: Implements Crystals-Kyber, a post-quantum cryptographic algorithm for secure data transmission.
- **Comprehensive Logging**: Utilizes a colored logging system for better readability and monitoring of system operations.

## Technologies Used

- **Python**: Core programming language for development.
- **PySpark**: For processing large-scale data.
- **ZeroMQ**: For efficient message queuing and communication between components.
- **Crypto Libraries**: For implementing cryptographic functions (AES, RSA, Crystals-Kyber).
- **Ansible**: For automating system configuration and management tasks.

## Project Structure

```
Bodhi-Sec/
├── airs.py              # Main script for the Automated Incident Response System
├── config.ini           # Configuration file for system settings
├── final.py             # Final version of script
├── dashboard.py         # Dashboard for visualizing system metrics
├── ddos.py              # Module for DDoS simulation
└── test.py              # Unit tests for validating functionality
```

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Het-Joshi/NETRA.git
   cd Bodhi-Sec
   ```

2. **Configure the System**
   Edit `config.ini` to set your specific configurations such as thresholds for requests and time windows.

3. **Run the AIRS**
   Start the Automated Incident Response System using:
   ```bash
   python final.py
   ```

## Usage

Once the system is running, it will:
- Monitor network traffic for incoming data.
- Log any detected threats and share intelligence on the ZeroMQ network.
- Implement self-healing actions if a potential DDoS attack is detected.

You can send sample data to the system to test its functionality using a tool like Postman or cURL.

## Contribution

Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
