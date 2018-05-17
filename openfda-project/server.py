import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000
MAX_OPEN_REQUESTS = 5

socketserver.TCPServer.allow_reuse_address = True


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # send status code
        self.send_response(200)
        # send normal headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == "/":
            with open("search.html", "r") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif "searchDrug" in self.path:
            # get the parameters
            data = self.path.split("?")[1]
            drug = data.split("&")[0].split("=")[1]
            # limit = data.split("&")[1].split("=")[1]

            # limit = 10 by default
            if "limit" in self.path:
                limit = self.path.split("=")[2]
                if limit == '':
                    limit = '10'
            else:
                limit = '10'

            # comunication  with openFDA API
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?search=active_ingredient=" + drug + "&limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            # extract the data from drugs item
            message = ''
            for i in range(len(drugs['results'])):
                try:
                    message += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</ol>'

                except KeyError:
                    message += '<ol>' + str(i + 1) + '. ' + ('Unknown') + '</ol>'

            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))


        elif "searchCompany" in self.path:
            data = self.path.split("?")[1]
            comp = data.split("&")[0].split("=")[1]

            if "limit" in self.path:
                limit = self.path.split("=")[2]
                if self.path.split("=")[2] == '':
                    limit = '10'
            else:
                limit = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?search=manufacturer_name:" + comp + "&limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            message = ''
            for i in range(len(drugs['results'])):
                try:
                    message += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</ol>'

                except KeyError:
                    message += '<ol>' + str(i + 1) + '. ' + ('Unknown') + '</ol>'

            self.wfile.write(bytes(message, "utf8"))

        elif "listDrugs" in self.path:
            data = self.path.split("?")[1]
            if "limit" in self.path:
                limit = data.split('=')[1]
                if limit == '':
                    limit = '10'
            else:
                limit = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            message = ''
            for i in range(len(drugs['results'])):
                try:
                    message += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</ol>'

                except KeyError:
                    message += '<ol>' + str(i + 1) + '. ' + ('Unknown') + '</ol>'

            self.wfile.write(bytes(message, "utf8"))

        elif "listCompanies" in self.path:
            data = self.path.split("?")[1]

            if "limit" in self.path:
                limit = data.split('=')[1]
                if limit == '':
                    limit = '10'
            else:
                limit = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            message = ''
            for i in range(len(drugs['results'])):
                try:
                    message += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['manufacturer_name'][
                        0] + '</ol>'

                except KeyError:
                    message += '<ol>' + str(i + 1) + '. ' + ('Unknown') + '</ol>'

            self.wfile.write(bytes(message, "utf8"))
        return


Handler = HTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")

# sandra salcedo
