from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html
import datetime

address = ('localhost', 8080)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 400 Response Test
        if self.path == "/400":
            self.setHTMLHeader(400)
            self.wfile.write("400".encode())
            return

        # Favicons disabled.
        if self.path.endswith('favicon.ico'):
            return

        # Add to HTML template with dictionary
        self.setHTMLHeader(200)
        page_dict = {}
        page_dict["test"] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        html = ""
        with open('./index.html', 'r', encoding='UTF-8') as f:
            html = transStr(f.read(), page_dict)
        self.wfile.write(html.encode())

    def do_POST(self):
        self.setHTMLHeader(200)

        # POST /action.php HTTP/1.0
        self.wfile.write(f'{self.command} {self.path} {self.protocol_version}\n'.replace("\n", "<br>").encode())
        # Host: 127.0.0.1:8080 ... 
        self.wfile.write(f'{self.headers}'.replace("\n", "<br>").encode())

        # Output Post requests
        postdata = self.rfile.read(int(self.headers['content-length'])).decode('utf-8')
        self.wfile.write(f"{html.escape(postdata)}<br>".encode())

        # URL Encode
        self.wfile.write("\n\n===== UTF-8 Encode =====\n".replace("\n", "<br>").encode())
        print(parse_qs(postdata))
        for key, value in parse_qs(postdata).items():
            self.wfile.write(f"{key}: {value[0]} \n".replace("\n", "<br>").encode())
    
    # Insert HTML headers
    def setHTMLHeader(self, code):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        return self

# Replace {% Key %} in HTML with dictionary value
def transStr(html, dict):
    for key, value in dict.items():
        html = html.replace('{% ' + key + ' %}', value)
    return html

with HTTPServer(address, MyHTTPRequestHandler) as server:
    server.serve_forever()