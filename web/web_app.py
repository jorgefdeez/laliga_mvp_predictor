import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8080
WEB_DIR = Path(__file__).resolve().parent

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

def main():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            url = f"http://localhost:{PORT}"
            print(f"==================================================")
            print(f" Servidor iniciado en: {url}")
            print(f" Pulsa Ctrl + C para detener el servidor")
            print(f"==================================================")
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"El puerto {PORT} ya está en uso. Abre en tu navegador: http://localhost:{PORT}")
            webbrowser.open(f"http://localhost:{PORT}")
        else:
            raise

if __name__ == "__main__":
    main()

