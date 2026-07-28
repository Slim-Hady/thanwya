#!/usr/bin/env python3
"""Simple HTTP server with gzip support for serving the results website."""

import gzip
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class GzipHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path) and path.endswith(".json"):
            with open(path, "rb") as f:
                raw = f.read()
            compressed = gzip.compress(raw, compresslevel=6)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(compressed)))
            self.end_headers()
            self.wfile.write(compressed)
        else:
            super().do_GET()


if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), GzipHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()
