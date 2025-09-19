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
    help="Size of the message (default: 500)",
)

args = parser.parse_args()

host = args.host
port = args.port
period = args.period
size = args.size

def send_stream(conn):
    overall_start_time = time.monotonic()
    while True:
        start_time = time.monotonic()
        values = [random.uniform(0.0, 1.0) for _ in range(size)]
        if len(values) <= 3:
            formatted = ", ".join(["{:.3f}".format(num) for num in values])
        else:
            formatted = "{:.3f}, {:.3f},... {:.3f}".format(values[0], values[1], values[-1])
        message = struct.pack(f"<{size}f", *values)
        timestamp = time.monotonic() - overall_start_time
        print("{:.0f}s: Sent {} values: {}".format(timestamp, len(values), formatted))

        conn.sendall(message)

        time.sleep(max(0, period - (time.monotonic() - start_time)))


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
            send_stream(conn)

