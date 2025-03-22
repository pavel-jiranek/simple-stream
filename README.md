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
