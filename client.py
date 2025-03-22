import socket
import struct
import argparse

parser = argparse.ArgumentParser(description='UDP Client that receives random numbers')
parser.add_argument('--host', default="127.0.0.1",
                   help='Host IP address (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default=1234,
                   help='Port number (default: 1234)')

args = parser.parse_args()

host = args.host
port = args.port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break

        num_messages = len(data) // 16 # 16 bytes per message = 2 doubles
        for i in range(num_messages):
            start_index = i * 16
            end_index = start_index + 16
            num1, num2 = struct.unpack('dd', data[start_index:end_index])
            print(f"Received: {num1}, {num2}")
