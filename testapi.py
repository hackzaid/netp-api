import http.client

conn = http.client.HTTPConnection("127.0.0.1:5000")

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer _7c9av_dd57HUovZja7PPH1RE9mxpM-LqLcGGQEhFlQ"
}

conn.request("GET", "/api/users", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
