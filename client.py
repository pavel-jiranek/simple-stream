import argparse
import socket
import struct

parser = argparse.ArgumentParser(description="UDP Client that receives random numbers")
parser.add_argument(
    "--host", default="127.0.0.1", help="Host IP address (default: 127.0.0.1)"
)
parser.add_argument(
    "--port", type=int, default=1234, help="Port number (default: 1234)"
)

args = parser.parse_args()

host = args.host
port = args.port

format_string = "fBI" * 10
item_size = struct.calcsize(format_string)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting...")
    s.connect((host, port))
    print("Connected!")

    while True:
        data = s.recv(item_size)
        if not data:
            break

        print(f"Received {len(data)} bytes...")

        triplets = struct.unpack(format_string, data)
        print(f"Received triplet: ({triplets[0]:.3f}, {triplets[1]}, {triplets[2]})...")
