"""Vercel serverless function: POST /api/run — execute TinyTalk code."""
from http.server import BaseHTTPRequestHandler
import json
import time
import io
from contextlib import redirect_stdout

from api._tinytalk import run, ExecutionBounds, TinyTalkError


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)
        code = data.get("code", "")

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
            result_str = str(result) if result.type.value != "null" else ""

            self._json(200, {
                "success": True,
                "output": output,
                "result": result_str,
                "elapsed_ms": round(elapsed, 2),
            })

        except TinyTalkError as e:
            elapsed = (time.time() - start_time) * 1000
            self._json(200, {
                "success": False,
                "error": str(e),
                "output": stdout_capture.getvalue(),
                "elapsed_ms": round(elapsed, 2),
            })

        except SyntaxError as e:
            elapsed = (time.time() - start_time) * 1000
            self._json(200, {
                "success": False,
                "error": f"Syntax Error: {e}",
                "output": stdout_capture.getvalue(),
                "elapsed_ms": round(elapsed, 2),
            })

        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            self._json(200, {
                "success": False,
                "error": f"{type(e).__name__}: {e}",
                "output": stdout_capture.getvalue(),
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
