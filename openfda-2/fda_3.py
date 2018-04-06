import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?search=active_ingredient."acetylsalicylic+acid"', None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo2=repos['results']


print("The manufacturer´s name of the Aspirin is:", repo2[0]['openfda']['manufacturer_name'])









