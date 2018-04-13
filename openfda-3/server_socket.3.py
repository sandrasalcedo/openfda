import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
socketserver.TCPServer.allow_reuse_adress = True
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


# HTTPRequestHandler class
class  server_sandra(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        drugs = json.loads(repos_raw)

        message = 'List with the 10 drugs:'
        for i in range(len(drugs['results'])):
            try:
                message += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['generic_name'][0] + '</ol>'

            except KeyError:
                message += '<ol>' + str(i + 1) + '. ' + ('No generic name found') + '</ol>'

        # write the content
        self.wfile.write(bytes(message, "utf8"))

        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = server_sandra

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!!!!")

