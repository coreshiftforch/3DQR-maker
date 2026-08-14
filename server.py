# ローカル確認用の簡易サーバー。
# Three.js を ESモジュール(importmap)で読むので file:// では動かない。必ずこれ経由で開くこと。
#   python server.py        … http://localhost:8080
#   python server.py 8081   … ポートを変える
# ※ Windows でポート8090などは WinError 10013 で弾かれることがあるので既定は8080。
import http.server, socketserver, sys, os, webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')   # 編集がすぐ反映されるように
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


with Server(('', PORT), Handler) as httpd:
    url = f'http://localhost:{PORT}/'
    print(f'{url} で開いています（Ctrl+C で終了）')
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n終了しました')
