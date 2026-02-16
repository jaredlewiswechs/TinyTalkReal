"""Vercel serverless function: POST /api/run — execute TinyTalk code."""

import sys, os, json, time, io
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler

# Fix path so the package is importable
_api_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_api_dir)
sys.path = [p for p in sys.path if os.path.abspath(p) != _project_root]
sys.path.insert(0, os.path.dirname(_project_root))
import importlib as _il
if 'realTinyTalk' not in sys.modules:
    sys.modules['realTinyTalk'] = _il.import_module(os.path.basename(_project_root))

from realTinyTalk import run, ExecutionBounds
from realTinyTalk.runtime import TinyTalkError


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body) if body else {}
        code = data.get('code', '')

        stdout_capture = io.StringIO()
        start_time = time.time()

        try:
            bounds = ExecutionBounds(
                max_ops=1_000_000,
                max_iterations=100_000,
                max_recursion=500,
                timeout_seconds=10.0,
            )
            with redirect_stdout(stdout_capture):
                result = run(code, bounds)

            elapsed = (time.time() - start_time) * 1000
            output = stdout_capture.getvalue()
            result_str = str(result) if result.type.value != 'null' else ''

            resp = json.dumps({
                'success': True,
                'output': output,
                'result': result_str,
                'elapsed_ms': round(elapsed, 2),
            })
        except TinyTalkError as e:
            elapsed = (time.time() - start_time) * 1000
            resp = json.dumps({
                'success': False,
                'error': str(e),
                'output': stdout_capture.getvalue(),
                'elapsed_ms': round(elapsed, 2),
            })
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            resp = json.dumps({
                'success': False,
                'error': f"{type(e).__name__}: {e}",
                'output': stdout_capture.getvalue(),
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
