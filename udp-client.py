import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- UDP client logic ---
UDP_SERVER_IP = "sample-udp-server-py"  # Or actual server IP if needed
UDP_SERVER_PORT = 9999
MESSAGE = "Hello via UDP!"

def send_udp_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)  # Timeout after 3 seconds
    try:
        sock.sendto(MESSAGE.encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))
        print(f"📤 Sent: {MESSAGE}")
        data, addr = sock.recvfrom(1024)
        print(f"✅ Received reply from {addr}: {data.decode()}")
        return True
    except socket.timeout:
        print("❌ No response from UDP server (timeout)")
        return False
    except Exception as e:
        print(f"❌ Error sending UDP message: {e}")
        return False
    finally:
        sock.close()

# --- HTTP server with /health endpoint ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/health", "/udp-client"]:
            udp_ok = send_udp_message()
            if udp_ok:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Client OK - UDP server responded")
            else:
                self.send_response(503)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Client ERROR - No UDP server response")
        else:
            self.send_response(404)
            self.end_headers()

HTTP_PORT = 8080

def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"🌐 HTTP server listening on port {HTTP_PORT}...")
    httpd.serve_forever()

# --- Run HTTP server ---
if __name__ == "__main__":
    run_http_server()
