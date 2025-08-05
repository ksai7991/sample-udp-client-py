import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- UDP client logic ---
UDP_IP = "0.0.0.0"  # Replace with server IP if needed
UDP_PORT = 9999
MESSAGE = "Hello via UDP!"

def send_udp_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    print(f"📤 Sent: {MESSAGE}")

# --- HTTP server with /health endpoint ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/health", "/udp-client"]:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Client OK")
        else:
            self.send_response(404)
            self.end_headers()

HTTP_PORT = 8080

def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"🌐 HTTP server listening on port {HTTP_PORT}...")
    httpd.serve_forever()

# --- Run UDP client and HTTP server ---
if __name__ == "__main__":
    # First, send the UDP message
    send_udp_message()

    # Then, run HTTP server in a thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Keep main thread alive
    http_thread.join()
