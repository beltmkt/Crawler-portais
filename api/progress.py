from http.server import BaseHTTPRequestHandler
import json
import time

# Importar jobs do extract (simulado)
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
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        from urllib.parse import urlparse, parse_qs
        
        try:
            # Extrair jobId da URL
            query = urlparse(self.path).query
            params = parse_qs(query)
            job_id = params.get('jobId', [None])[0]
            
            if not job_id:
                response = {"error": "jobId é obrigatório"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            job = jobs.get(job_id)
            
            if not job:
                response = {"error": "Job não encontrado"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Calcular tempo decorrido
            elapsed = time.time() - job.get('startTime', time.time())
            
            response = {
                "status": job.get('status', 'running'),
                "total": job.get('total', 0),
                "processed": job.get('processed', 0),
                "photos": job.get('photos', 0),
                "logs": job.get('logs', []),
                "xml": job.get('xml', None),
                "elapsedTime": elapsed
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())
        return
