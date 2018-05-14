import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000
MAX_OPEN_REQUESTS = 5

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        if self.path == "/":
            with open("search.html", "r") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif "searchdrug" in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            list1 = []
            data = self.path.split("=")
            drug = data[0].split("=")[1]
            limit = data[1].split("=")[1]
            if limit == "":
                limit1 = "10"
                url = "/drug/label.json?search=active_ingredient:" + drug + ("=") + limit1
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                drugs = json.loads(drugs_raw)
                conn.close()

                for i in range(len(drugs['results'])):
                    try:
                        if 'openfda' in drugs['results'][i]:
                            list1.append(drugs['results'][i]['openfda']['active_ingredient'][0])
                    except KeyError:
                        list1.append('No drugs')
                with open("blank.html", "w") as f:
                    f.write("<!doctype html>" + "<html>" + "<body>" + "<ul>")
                    for element in list1:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write("</ul>" + "</body>" + "</html>")
                with open("blank.html", "r") as f:
                    file = f.read()
                self.wfile.write(bytes(file, "utf8"))



        elif "searchcompany" in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.split("=")
            company = data[0].split("=")[1]
            limit = data[1].split("=")[1]
            url = "/drug/label.json?search=manufacturer_name:" + company + ("=") + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            company_raw = r1.read().decode("utf-8")
            conn.close()
            companies = json.loads(company_raw)
            list2 = []
            for i in range(len(companies['results'])):
                list2.append(companies['results'][i]['openfda']['manufacturer_name'][0])
            with open("blank.html", "w") as f:
                f.write("<!doctype html>" + "<html>" + "<body>" + "<ul>")
                for element in list2:
                    element_1 = "<li>" + element + "</li>" + "\n"
                    f.write(element_1)
                f.write("</ul>" + "</body>" + "</html>")
            with open("blank.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))

        elif "listdrugs" in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.split("=")
            limit = data[1].split("=")[1]
            url = "/drug/label.json?" + ("limit=") + limit
            #print(url)
            #print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drug_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(drug_raw)
            list3 = []
            print(drugs)
            for i in range(len(drugs['results'])):
                try:
                    if 'openfda' in drugs['results'][i]:
                        list3.append(drugs['results'][i]['openfda']["brand_name"][0])
                except KeyError:
                    list3.append('Unknown')

            with open("blank.html", "w") as f:
                f.write("<!doctype html>" + "<html>" + "<body>" + "<ul>")
                for element in list3:
                    element_1 = "<li>" + element + "</li>" + "\n"
                    f.write(element_1)
                f.write("</ul>" + "</body>" + "</html>")

            with open("blank.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))

        elif "listcompanies" in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.split("=")
            limit = data[1].split("=")[1]
            url = "/drug/label.json?" + "limit=" + limit
            #print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            company_raw = r1.read().decode("utf-8")
            conn.close()
            companies = json.loads(company_raw)
            list4 = []
            for i in range(len(companies['results'])):
                try:
                    if "openfda" in companies['results'][i]:
                        list4.append(companies['results'][i]['openfda']["manufacturer_name"][0])
                except KeyError:
                    list4.append("Unknown")

            with open("blank.html", "w") as f:
                f.write("<!doctype html>" + "<html>" + "<body>" + "<ul>")
                for element in list4:
                    element_1 = "<li>" + element + "</li>" + "\n"
                    f.write(element_1)
                f.write("</ul>" + "</body>" + "</html>")

            with open("blank.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))





Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()
