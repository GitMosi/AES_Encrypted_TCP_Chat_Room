# SERVER CODE
# Update 1.1 AES Encryption Now Included :p
# AES Block Cipher 16 bytes block size as supported by pyaes
# You Can Change the Port Server Listens by passing argument in command line directly
# Server Code To be Started before Client, or Connection will be refused

import os
try:
    import pyaes
except ImportError:
    print("Install pyaes library!")
    print("Windows : python -m pip install pyaes")
    print("Linux   : pip install pyaes ")
    exit()
import sys
import socket
import threading
import hashlib
import json
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5555
show_ciphertext = input('[+] Display Cipher Text? (y/n): ').strip().lower() == 'y'

if len(sys.argv) == 1:
    PORT = 5555
elif len(sys.argv) == 2:
    PORT = int(sys.argv[1])

print("[+] Server Running")
print("[+] Allowing All Incoming Connections")
print("[+] PORT " + str(PORT))
print("[+] Waiting For Connection...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('[+] Connected by ', addr)

key = str(input('[+] AES Pre-Shared-Key for the Connection : '))
hashed = hashlib.sha256(key.encode()).digest()
aes = pyaes.AES(hashed)

def verify_and_display(recv_dict):
    timestamp = recv_dict['timestamp']
    recv_hash = recv_dict['hash']
    message = recv_dict['message']
    mess_hash = hashlib.sha256(str(message).encode('utf-8')).hexdigest()
    SET_LEN = 80
    if mess_hash == recv_hash:
        tag = '☑'
    else:
        tag = '☒'
    spaces = SET_LEN - len(str(message)) - len('Received : ') - 1
    if spaces > 0:
        space = ' ' * spaces
        sentence = 'Received : ' + str(message) + space + tag + '  ' + timestamp
        print(sentence)

def process_bytes(bytess):
    ret = []
    while len(bytess) >= 16:
        byts = bytess[:16]
        ret.append(byts)
        bytess = bytess[16:]
    return ret

def process_text(data):
    streams = []
    while len(data) > 0:
        if len(data) >= 16:
            stream = data[:16]
            data = data[16:]
        else:
            stream = data + ("~" * (16 - len(data)))
            data = ''
        stream_bytes = [ord(c) for c in stream]
        streams.append(stream_bytes)
    return streams

class myThread(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.threadID = id

    def stop(self):
        self.is_alive = False

    def run(self):
        print("[+] Listening On Thread " + str(self.threadID))
        while True:
            try:
                data = conn.recv(1024)
                if data != b"":
                    mess = ''
                    processed_data = process_bytes(data)
                    for dat in processed_data:
                        decrypted = aes.decrypt(dat)
                        for ch in decrypted:
                            if chr(ch) != '~':
                                mess += str(chr(ch))
                    try:
                        data_recv = json.loads(mess)
                        verify_and_display(data_recv)
                    except:
                        print('Unrecognised Data or Broken PIPE')
            except ConnectionResetError:
                print('Broken PIPE!')
                exit(0)

Listening_Thread = myThread(1)
Listening_Thread.daemon = True
Listening_Thread.start()

while True:
    try:
        sending_data = str(input(""))
    except KeyboardInterrupt:
        conn.close()
        exit(-1)
    if sending_data == "quit()":
        Listening_Thread.stop()
        conn.close()
        exit()
    timestamp = str(datetime.now())[11:19]
    mess_hash = hashlib.sha256(str(sending_data).encode('utf-8')).hexdigest()
    send_data = {
        "timestamp": timestamp,
        "message": sending_data,
        "hash": mess_hash
    }
    send_json_string = json.dumps(send_data)
    sending_bytes = process_text(send_json_string)
    enc_bytes = []
    for byte in sending_bytes:
        ciphertext = aes.encrypt(byte)
        enc_bytes += bytes(ciphertext)

        # Show cipher text if the option is set
        if show_ciphertext:
            print("Cipher Text:", ciphertext)

    conn.send(bytes(enc_bytes))
conn.close()