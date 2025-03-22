# A Simple TCP Stream

A simple TCP server-client implementation where the server streams a fixed amount of real floating point numbers to the connected client.

## Usage

### Starting the Server
```bash
python server.py [--host HOST] [--port PORT]

# Examples:
python server.py                    # Run with default settings (0.0.0.0:1234)
python server.py --port 5000        # Run on port 5000
python server.py --host 127.0.0.1   # Run on specific host
```

### Starting the Client
```bash
python client.py [--host HOST] [--port PORT]

# Examples:
python client.py                    # Connect to 127.0.0.1:1234
python client.py --port 5000        # Connect to 127.0.0.1:5000
python client.py --host 192.168.1.1 # Connect to remote server
```

## Command Line Arguments

### Server
- `--host`: Host IP address to bind to (default: 0.0.0.0)
- `--port`: Port number to listen on (default: 1234)

### Client
- `--host`: Server IP address to connect to (default: 127.0.0.1)
- `--port`: Server port number to connect to (default: 1234)

## Data Format
The server sends pairs of double-precision floating-point numbers (8 bytes each) in the binary format. 
Each message consists of 16 bytes (2 doubles precision floating point numbers).

## Examples

### Scenario 1: Local Testing (Same Machine)
In this scenario, both server and client run on the same machine. Open two terminal windows:

Terminal 1 (Server):
```bash
python server.py
# Output: Server streaming on 0.0.0.0:1234
# Output: Waiting for client connection...
```

Terminal 2 (Client):
```bash
python client.py
# Output: Received: 45.32, 78.91 from 127.0.0.1:1234
# Output: Received: 12.45, 67.89 from 127.0.0.1:1234
# (continuous stream of numbers...)
```

### Scenario 2: Network Setup (Different Machines)
In this scenario, the server runs on one machine (e.g., IP: 192.168.1.100) and the client on another machine in the same network.

Machine 1 (Server):
```bash
python server.py --host 192.168.1.100
# Output: Server streaming on 192.168.1.100:1234
# Output: Waiting for client connection...
```

Machine 2 (Client):
```bash
python client.py --host 192.168.1.100
# Output: Received: 23.67, 91.45 from 192.168.1.100:1234
# Output: Received: 56.78, 34.12 from 192.168.1.100:1234
# (continuous stream of numbers...)
```

Note: Make sure both machines are on the same network and any necessary firewall rules allow the connection on the specified port.
