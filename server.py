import argparse
import random
import socket
import struct
import time

parser = argparse.ArgumentParser(description="UDP Server that sends random numbers")
parser.add_argument(
    "--host", default="0.0.0.0", help="Host IP address (default: 0.0.0.0)"
)
parser.add_argument(
    "--port", type=int, default=1234, help="Port number (default: 1234)"
)

args = parser.parse_args()

host = args.host
port = args.port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    print(f"Server streaming on {host}:{port}")

    while True:
        print("Waiting for client connection...")
        conn, addr = s.accept()
        print(f"Client connected from {addr}")

        with conn:
            try:
                while True:
                    num1 = random.randint(-2147483648, 2147483647)
                    num2 = random.randint(-2147483648, 2147483647)
                    message = struct.pack("ii", num1, num2)

                    conn.sendall(message)
                    print(f"Sent: {num1}, {num2} to {addr}")

                    time.sleep(0.1)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                print(f"Client disconnected from {addr}")
