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
                    triplets = []
                    for _ in range(10):
                        float_val = random.uniform(-0.1, 0.1)
                        byte_val = random.randint(0, 1)
                        uint32_val = random.randint(0, 2**32 - 1)

                        triplets.extend([float_val, byte_val, uint32_val])

                    format_string = "fBI" * 10
                    message = struct.pack(format_string, *triplets)

                    conn.sendall(message)
                    print(
                        f"Sent triplet: ({triplets[0]:.3f}, {triplets[1]}, {triplets[2]})... to {addr}"
                    )

                    time.sleep(0.1)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                print(f"Client disconnected from {addr}")
