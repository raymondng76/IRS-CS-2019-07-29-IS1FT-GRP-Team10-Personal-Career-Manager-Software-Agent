import requests

def getjson(url):
    resp = requests.get(url)
    if resp.ok:
        return resp.json()