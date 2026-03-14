from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# Importar jobs do extract
from extract import jobs

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_GET(self):
        try:
            # Extrair jobId da URL
            query = urlparse(self.path).query
            params = parse_qs(query)
            job_id = params.get('jobId', [None])[0]
            
            if not job_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "jobId é obrigatório"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            job = jobs.get(job_id)
            
            if not job or not job.get('xml'):
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "XML não encontrado"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.send_header('Content-Disposition', f'attachment; filename="imoveis_{job_id}.xml"')
            self.end_headers()
            
            self.wfile.write(job['xml'].encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())
        return
