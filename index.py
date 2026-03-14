from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "ok",
            "message": "Chaves Exporter API está funcionando!",
            "endpoints": {
                "login": "/api/login",
                "extract": "/api/extract",
                "progress": "/api/progress?jobId=XXX",
                "download": "/api/download?jobId=XXX"
            }
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
