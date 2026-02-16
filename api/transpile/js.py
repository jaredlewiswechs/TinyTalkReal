"""Vercel serverless function: POST /api/transpile/js — transpile TinyTalk to JS."""
from http.server import BaseHTTPRequestHandler
import json
import time

from api._tinytalk import Lexer, Parser, PythonEmitter


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)
        code = data.get("code", "")
        include_runtime = data.get("include_runtime", True)

        start_time = time.time()
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            emitter = PythonEmitter(include_runtime=include_runtime)
            js_code = emitter.emit(ast)
            elapsed = (time.time() - start_time) * 1000
            self._json(200, {
                "success": True,
                "code": js_code,
                "language": "javascript",
                "elapsed_ms": round(elapsed, 2),
            })
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            self._json(200, {
                "success": False,
                "error": f"{type(e).__name__}: {e}",
                "elapsed_ms": round(elapsed, 2),
            })

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)
