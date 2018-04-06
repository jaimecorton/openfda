import http.server
import socketserver
import json

PORT = 8006

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        drugs = json.loads(repos_raw)

        drugs = drugs['results']
        drugs_id = "<ol>" + drugs[0]['id'] + "</ol>" + \
                   "<ol>" + drugs[1]['id'] + "</ol>" + \
                   "<ol>" + drugs[2]['id'] + "</ol>" + \
                   "<ol>" + drugs[3]['id'] + "</ol>" + \
                   "<ol>" + drugs[4]['id'] + "</ol>" + \
                   "<ol>" + drugs[5]['id'] + "</ol>" + \
                   "<ol>" + drugs[6]['id'] + "</ol>" + \
                   "<ol>" + drugs[7]['id'] + "</ol>" + \
                   "<ol>" + drugs[8]['id'] + "</ol>" + \
                   "<ol>" + drugs[9]['id'] + "</ol>"



        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = drugs_id
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
