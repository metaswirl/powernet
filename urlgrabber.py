import requests
API_KEY = "dhSMYpE5d052v7FgnBSs8ecKqYFuDINwHCicvstMP8g"
URL1 = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/Web?Query=%27"
URL2 = "%27&$top=50&$format=json"

def geturls(query):
    urls=[]
    r=requests.get(URL1+query+URL2, auth=("", API_KEY))
    for url in r.json()["d"]["results"]:
        urls.append(url["Url"])
    return urls
