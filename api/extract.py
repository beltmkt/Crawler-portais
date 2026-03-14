from http.server import BaseHTTPRequestHandler
import json
import time
import uuid
import subprocess
import threading
import os

# Armazenamento em memória (em produção, use Redis)
jobs = {}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            sessionToken = data.get('sessionToken')
            anuncios = data.get('anuncios', [])
            
            if not sessionToken or not anuncios:
                response = {"success": False, "error": "sessionToken e anuncios obrigatórios"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Criar job ID
            job_id = f"job_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            
            # Inicializar job
            jobs[job_id] = {
                "status": "pending",
                "total": len(anuncios),
                "processed": 0,
                "photos": 0,
                "results": [],
                "logs": [],
                "startTime": time.time()
            }
            
            # Iniciar processamento em background
            thread = threading.Thread(target=processar_anuncios, args=(job_id, anuncios))
            thread.daemon = True
            thread.start()
            
            response = {
                "success": True,
                "jobId": job_id,
                "message": "Extração iniciada"
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            response = {"success": False, "error": str(e)}
            self.wfile.write(json.dumps(response).encode())
        return

def processar_anuncios(job_id, anuncios):
    """Processa os anúncios (simulado - aqui você chamaria seu crawler)"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["logs"].append({"message": "🚀 Iniciando processamento...", "timestamp": time.time()})
        
        results = []
        total_fotos = 0
        
        for i, anuncio in enumerate(anuncios):
            jobs[job_id]["logs"].append({
                "message": f"⏳ Processando anúncio {i+1}/{len(anuncios)}: {anuncio.get('id', '')}",
                "timestamp": time.time()
            })
            
            # SIMULAÇÃO: Aqui você chamaria seu crawler real
            # Exemplo: subprocess.run(['python', 'crawler/crawler_chavesnamao.py', anuncio['url']])
            
            time.sleep(2)  # Simular processamento
            
            # Dados simulados
            fotos = [f"https://exemplo.com/foto{i}_{j}.jpg" for j in range(5)]
            
            results.append({
                "id": anuncio.get('id', f"ID_{i}"),
                "titulo": anuncio.get('titulo', 'Imóvel'),
                "fotos": fotos
            })
            
            total_fotos += len(fotos)
            
            jobs[job_id]["processed"] = i + 1
            jobs[job_id]["photos"] = total_fotos
            jobs[job_id]["results"] = results
            
            jobs[job_id]["logs"].append({
                "message": f"✅ Anúncio {i+1} processado - {len(fotos)} fotos",
                "timestamp": time.time()
            })
        
        # Gerar XML simulado
        xml = gerar_xml_simulado(results)
        jobs[job_id]["xml"] = xml
        jobs[job_id]["status"] = "completed"
        
        jobs[job_id]["logs"].append({
            "message": "✅ Extração concluída com sucesso!",
            "timestamp": time.time()
        })
        
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["logs"].append({
            "message": f"❌ Erro: {str(e)}",
            "timestamp": time.time()
        })

def gerar_xml_simulado(imoveis):
    """Gera XML simulado"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<lista>\n'
    for imovel in imoveis:
        xml += '  <imovel>\n'
        xml += f'    <id>{imovel["id"]}</id>\n'
        xml += f'    <titulo>{imovel["titulo"]}</titulo>\n'
        xml += '    <fotos>\n'
        for foto in imovel["fotos"]:
            xml += f'      <foto>{foto}</foto>\n'
        xml += '    </fotos>\n'
        xml += '  </imovel>\n'
    xml += '</lista>'
    return xml
