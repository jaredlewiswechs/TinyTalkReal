"""Vercel serverless function: POST /api/transpile/js — transpile TinyTalk to JS."""

import sys, os, json, time
from http.server import BaseHTTPRequestHandler

_api_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_api_dir))
sys.path = [p for p in sys.path if os.path.abspath(p) != _project_root]
sys.path.insert(0, os.path.dirname(_project_root))
import importlib as _il
if 'realTinyTalk' not in sys.modules:
    sys.modules['realTinyTalk'] = _il.import_module(os.path.basename(_project_root))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body) if body else {}
        code = data.get('code', '')
        include_runtime = data.get('include_runtime', True)

        start_time = time.time()
        try:
            from realTinyTalk.lexer import Lexer
            from realTinyTalk.parser import Parser
            from realTinyTalk.emitter import PythonEmitter

            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            emitter = PythonEmitter(include_runtime=include_runtime)
            js_code = emitter.emit(ast)
            elapsed = (time.time() - start_time) * 1000

            resp = json.dumps({
                'success': True,
                'code': js_code,
                'language': 'javascript',
                'elapsed_ms': round(elapsed, 2),
            })
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            resp = json.dumps({
                'success': False,
                'error': f"{type(e).__name__}: {e}",
                'elapsed_ms': round(elapsed, 2),
            })

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(resp.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
