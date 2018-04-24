import http.server
import http.client
import socketserver
import json

socketserver.TCPServer.allow_reuse_address = True

PORT = 8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            with open("openfda.html") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))

        elif "searchDrug" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=active_ingredient:' + drug + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            total_drug = ""
            for drug in drugs['results']:
                drugs_id = "<ol>" + drug['id'] + "</ol>"
                total_drug = total_drug + drugs_id
            self.wfile.write(bytes(total_drug, "utf8"))

        elif "searchCompany" in self.path:
            params = self.path.split("?")[1]
            company = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=openfda.manufacturer_name:' + company + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            total_drug = ""
            for drug in drugs['results']:
                drugs_id = "<ol>" + drug['id'] + "</ol>"
                total_drug = total_drug + drugs_id
            self.wfile.write(bytes(total_drug, "utf8"))

        elif "listDrugs" in self.path:
            headers = {'User-Agent': 'http-client'}
            params = self.path.split("?")[1]
            limit = params.split("&")[0].split("=")[1]

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json' + "?limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            listDrugs = "<html>" + \
                       "<body>" + \
                       "<ul>"

            for drug in drugs['results']:
                listDrugs += "<li>" + drug['id']
                listDrugs += "</li>"
            listDrugs += "</ul>" + \
                        "</body>" + \
                        "</html>"

            self.wfile.write(bytes(listDrugs, "utf8"))


        elif "listCompanies" in self.path:
            headers = {'User-Agent': 'http-client'}
            params = self.path.split("?")[1]
            limit = params.split("&")[0].split("=")[1]

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?limit='+ limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)

            listCompanies = "<html>" + \
                          "<body>" + \
                          "<ul>"

            for drug in drugs['results']:
                if 'manufacturer_name' in drug['openfda']:
                    listCompanies += "<li>" + drug['openfda']['manufacturer_name'][0]
                else:
                    listCompanies += "<li>" + "Not available info"
                listCompanies += "</li>"

            listCompanies += "</ul>" + \
                           "</body>" + \
                           "</html>"

            self.wfile.write(bytes(listCompanies, "utf8"))

        elif "listWarnings" in self.path:
            headers = {'User-Agent': 'http-client'}
            params = self.path.split("?")[1]
            limit = params.split("&")[0].split("=")[1]

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?limit='+ limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)

            listWarnings = "<html>" + \
                          "<body>" + \
                          "<ul>"

            for drug in drugs['results']:
                if 'warnings' in drug:
                    listWarnings += "<li>" + drug['warnings'][0]
                else:
                    listWarnings += "<li>"+"Not available info"
                listWarnings += "</li>"

            listWarnings += "</ul>" + \
                           "</body>" + \
                           "</html>"

            self.wfile.write(bytes(listWarnings, "utf8"))



        return


Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
#MADEBYJAIMECORTÓN
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()