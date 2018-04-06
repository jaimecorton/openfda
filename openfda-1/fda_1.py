import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
repo1=repos['meta']
repo2=repos['results']


print("That´s the drug id", repo2[0]['openfda']['spl_id'])
print("That´s the drug purpose", repo2[0]['purpose'])
print("That´s the drug manufacturer's name", repo2[0]['openfda']['manufacturer_name'])




