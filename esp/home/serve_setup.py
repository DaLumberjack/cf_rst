#!/usr/bin/env python3
"""
Simple HTTP server to serve the CommuniFarm setup web interface
Run this script and navigate to http://localhost:8000 to access the setup interface
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class SetupHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/setup_web.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/configure':
            # Handle configuration POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # In a real implementation, this would process the configuration
            # and generate the ESPHome YAML file
            print("Received configuration:", post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Configuration saved"}')
        else:
            super().do_POST()

def main():
    PORT = 8000
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    with socketserver.TCPServer(("", PORT), SetupHTTPRequestHandler) as httpd:
        print(f"🌱 CommuniFarm Setup Server")
        print(f"📡 Server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {script_dir}")
        print(f"🌐 Open your browser and go to: http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        
        # Try to open the browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
