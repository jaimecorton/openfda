import http.server
import http.client
import socketserver
import json

socketserver.TCPServer.allow_reuse_address = True

PORT = 8005

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            with open("search.html") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))

        elif "search" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=generic_name:' + drug + "&limit=" + limit, None, headers)
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

        return


Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
#MADEBYJAIMECORTÓN
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever())

