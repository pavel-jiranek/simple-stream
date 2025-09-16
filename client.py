"""
A simple TCP client that receives a fixed amount of real floating point numbers from the server.
"""

import argparse
import socket
import struct
import time

parser = argparse.ArgumentParser(description="UDP Client that receives random numbers")
parser.add_argument(
    "--host",
    default="127.0.0.1",
    help="Host IP address (default: 127.0.0.1)",
)
parser.add_argument(
    "--port",
    type=int,
    default=1234,
    help="Port number (default: 1234)",
)
parser.add_argument(
    "--rate",
    type=float,
    default=0.1,
    help="Rate of receiving numbers (default: 0.1)",
)

args = parser.parse_args()

host = args.host
port = args.port
rate = args.rate
bufsize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {host}:{port}...")
    s.connect((host, port))

    overall_start_time = time.monotonic()
    while True:
        try:
            start_time = time.monotonic()
            data = s.recv(bufsize)
            if not data:
                print("No data received")
                break

            unpacked = struct.iter_unpack("<f", data)
            values = [item[0] for item in unpacked]
            formatted = ", ".join([f"{num:.3f}" for num in values])
            timestamp = time.monotonic() - overall_start_time
            print(f"{timestamp:.0f}s: Received {len(values)} values: {formatted}")

            time.sleep(max(0, rate - (time.monotonic() - start_time)))
        except Exception as e:
            print(f"Error receiving data: {e}")
            pass
