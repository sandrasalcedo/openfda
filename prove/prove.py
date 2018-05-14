import http.server
import socketserver
import json
import http.client


# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True

notexist = "unknown"


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        first = "<!doctype html>" + "<html>" + "<body>" + "<ul>"
        last = "</ul>" + "</body>" + "</html>"

        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open("search1.html", "r") as f:
                    message = f.read()
                    self.wfile.write(bytes(message, "utf8"))

            elif "searchDrug" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list1 = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                if "&" in self.path:
                    data = self.path.split("?")[1]
                    drug = data.split("&")[0].split("=")[1]
                    limit = data.split("&")[1].split("=")[1]
                    if limit =="":
                        limit = "10"
                    url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        if 'active_ingredient' in drugs1['results'][i]:
                            list1.append(drugs1['results'][i]['active_ingredient'][0])
                        else:
                            list1.append("This index has no drug")
                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list1:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))

                else:
                    limite = "10"
                    data = self.path.split("?")[1]
                    drug = data.split("&")[0].split("=")[1]
                    url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limite
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        if 'active_ingredient' in drugs1['results'][i]:
                            list1.append(drugs1['results'][i]['active_ingredient'][0])
                        else:
                            list1.append("This index has no drug")
                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list1:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))




            elif "searchCompany" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")


                if "&" in self.path:
                    data = self.path.split("?")[1]
                    company = data.split("&")[0].split("=")[1]
                    limit = data.split("&")[1].split("=")[1]
                    if limit == "":
                        limit = "10"
                    url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    company_raw = r1.read().decode("utf-8")
                    conn.close()
                    company = json.loads(company_raw)
                    companies1 = company

                    for i in range(len(companies1['results'])):
                        if 'active_ingredient' in companies1['results'][i]:
                            list.append(companies1['results'][i]['openfda']["manufacturer_name"][0])
                        else:
                            list.append("This index has no manufacturer name")
                    with open("practice.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))

                else:
                    data = self.path.split("?")[1]
                    company = data.split("&")[0].split("=")[1]
                    limite = "10"
                    url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limite
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    company_raw = r1.read().decode("utf-8")
                    conn.close()
                    company = json.loads(company_raw)
                    companies1 = company

                    for i in range(len(companies1['results'])):
                        if 'active_ingredient' in companies1['results'][i]:
                            list.append(companies1['results'][i]['openfda']["manufacturer_name"][0])
                        else:
                            list.append("This index has no manufacturer name")
                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))


            elif "listDrugs" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                drug = self.path.split("?")[1]
                limit = drug.split("=")[1]
                if limit == "":
                    limit = "10"
                    url = "/drug/label.json?" + "limit=" + limit
                    print(url)
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        try:
                            if "openfda" in drugs1["results"][i]:
                                list.append(drugs1['results'][i]['openfda']["brand_name"][0])
                        except KeyError:
                            list.append("Unknown")

                    with open("practice.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))
                else:
                    url = "/drug/label.json?" + "limit=" + limit
                    print(url)
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        try:
                            if "openfda" in drugs1["results"][i]:
                                list.append(drugs1['results'][i]['openfda']["brand_name"][0])
                        except KeyError:
                            list.append("Unknown")

                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
                        file = f.read()

                    self.wfile.write(bytes(file, "utf8"))


            elif "listCompanies" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                drug = self.path.split("?")[1]
                limit = drug.split("=")[1]
                if limit == "":
                    limit = "10"
                    url = "/drug/label.json?" + "limit=" + limit
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        try:
                            if "openfda" in drugs1["results"][i]:
                                list.append(drugs1['results'][i]['openfda']["manufacturer_name"][0])
                        except KeyError:
                            list.append("Unknown")

                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("practice.html", "r") as f:
                        file = f.read()
                    self.wfile.write(bytes(file, "utf8"))
                else:
                    url = "/drug/label.json?" + "limit=" + limit
                    conn.request("GET", url, None, headers)
                    r1 = conn.getresponse()
                    drugs_raw = r1.read().decode("utf-8")
                    conn.close()
                    drug = json.loads(drugs_raw)
                    drugs1 = drug

                    for i in range(len(drugs1['results'])):
                        try:
                            if "openfda" in drugs1["results"][i]:
                                list.append(drugs1['results'][i]['openfda']["manufacturer_name"][0])
                        except KeyError:
                            list.append("Unknown")

                    with open("empty.html", "w") as f:
                        f.write(first)
                        for element in list:
                            element_1 = "<li>" + element + "</li>" + "\n"
                            f.write(element_1)
                        f.write(last)
                    with open("empty.html", "r") as f:
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