"""
A simple TCP server that streams a fixed amount of real floating point numbers
to the connected client at a fixed rate.
"""

import argparse
import random
import socket
import struct
import time

parser = argparse.ArgumentParser(description="TCP Server that sends random numbers")
parser.add_argument(
    "--host",
    default="0.0.0.0",
    help="Host IP address (default: 0.0.0.0)",
)
parser.add_argument(
    "--port",
    type=int,
    default=1234,
    help="Port number (default: 1234)",
)
parser.add_argument(
    "--period",
    type=float,
    default=0.1,
    help="Period of sending numbers (default: 0.1)",
)
parser.add_argument(
    "--size",
    type=int,
    default=10,
    help="Size of the message (default: 10)",
)

args = parser.parse_args()

host = args.host
port = args.port
period = args.period
size = args.size

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
            overall_start_time = time.monotonic()
            try:
                while True:
                    start_time = time.monotonic()
                    values = [random.uniform(0.0, 1.0) for _ in range(size)]
                    formatted = ", ".join([f"{num:.3f}" for num in values])
                    message = struct.pack(f"<{size}f", *values)
                    timestamp = time.monotonic() - overall_start_time
                    print(f"{timestamp:.0f}s: Sent {len(values)} values: {formatted}")

                    conn.sendall(message)

                    time.sleep(max(0, period - (time.monotonic() - start_time)))
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                print(f"Client disconnected from {addr}")
