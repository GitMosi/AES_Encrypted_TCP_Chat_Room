# AES Encrypted TCP Chat Room

## Overview
Welcome to the AES Encrypted Client-Server TCP Chat Room project! This project demonstrates a simple yet robust implementation of a chat application using TCP sockets, enhanced by the security of AES encryption. The project consists of both a server and a client component, allowing for real-time, secure messaging between users.

## Features
- **AES Encryption**: All messages are encrypted using the AES block cipher, ensuring that data remains confidential during transmission.
- **Multi-threading Support**: Both server and client applications can handle multiple connections simultaneously, improving performance and user experience.
- **Data Integrity Check**: Each message sent includes a hash to verify its integrity upon receipt, providing an additional layer of security.
- **User Interaction**: Simple command line interface for initiating connections and sending messages.

## Getting Started

### Requirements
- Python 3.x
- `pyaes` library for AES encryption (install using `pip install pyaes`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/GitMosi/AES_Encrypted_TCP_Chat_Room.git
