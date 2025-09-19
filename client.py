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
    "--period",
    type=float,
    default=0.1,
    help="Period of receiving numbers (default: 0.1)",
)
parser.add_argument(
    "--size",
    type=int,
    default=10,
    help="Expected size of the message (default: 10)",
)

args = parser.parse_args()

host = args.host
port = args.port
period = args.period
bufsize = args.size * struct.calcsize("<f")

def receive_stream(s):
    overall_start_time = time.monotonic()
    while True:
        start_time = time.monotonic()
        data = s.recv(bufsize)
        if not data:
            print("No data received")
            break

        unpacked = struct.iter_unpack("<f", data)
        values = [item[0] for item in unpacked]
        if len(values) <= 3:
            formatted = ", ".join(["{:.3f}".format(num) for num in values])
        else:
            formatted = "{:.3f}, {:.3f},... {:.3f}".format(values[0], values[1], values[-1])
        timestamp = time.monotonic() - overall_start_time
        print("{:.0f}s: Received {} values: {}".format(timestamp, len(values), formatted))

        time.sleep(max(0, period - (time.monotonic() - start_time)))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {host}:{port}...")
    s.connect((host, port))

    receive_stream(s)

