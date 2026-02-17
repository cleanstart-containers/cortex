"""Serve test-metric.txt at :9090/metrics for Prometheus scrape (then remote_write to Cortex)."""
import http.server
import socketserver

PORT = 9090


class MetricsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics" or self.path == "/":
            try:
                with open("test-metric.txt", "rb") as f:
                    body = f.read()
            except FileNotFoundError:
                body = b"# No test-metric.txt found\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MetricsHandler) as httpd:
        print(f"Serving metrics at http://0.0.0.0:{PORT}/metrics")
        httpd.serve_forever()
