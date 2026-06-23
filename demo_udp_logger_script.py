import socket
import signal
import sys

# Configuration
UDP_IP = "0.0.0.0"  # Listens on all available network interfaces
UDP_PORT = 5005     # MUST match the port XipppyServer.py is broadcasting to
BUFFER_SIZE = 65535 # Max UDP packet size
OUTPUT_FILE = "ripple_udp_stream.bin"

# Graceful exit handler
is_running = True
def signal_handler(sig, frame):
    global is_running
    print("\nStopping stream and closing file...")
    is_running = False

signal.signal(signal.SIGINT, signal_handler)

def main():
    # 1. Initialize the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"Listening for Ripple UDP stream on port {UDP_PORT}...")
    print("Press Ctrl+C to stop recording.")

    # 2. Open file in append-binary mode
    with open(OUTPUT_FILE, "ab") as f:
        while is_running:
            try:
                # Receive data
                data, addr = sock.recvfrom(BUFFER_SIZE)
                
                # Write raw bytes directly to file to minimize latency
                f.write(data)
                
            except socket.error as e:
                print(f"Socket error: {e}")
                break

    sock.close()
    print("Data logging complete.")

if __name__ == "__main__":
    main()