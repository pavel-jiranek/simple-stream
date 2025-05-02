import argparse
import random
import socket
import struct
import time
import numpy as np

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

data = np.linspace(-0.1, 0.1, 100)
pos = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                    nums = []
                    for _ in range(10):
                        nums.append(data[pos])
                        pos += 1
                        pos %= len(data)

                    message = struct.pack(f"{len(nums)}f", *nums)

                    conn.sendall(message)
                    print(f"Sent: {nums[0]}... to {addr}")

                    time.sleep(0.1)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                print(f"Client disconnected from {addr}")
