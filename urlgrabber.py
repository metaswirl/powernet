import requests
API_KEY = "CX0caiCq6wdY33dBrTu7lWx3YgfD9Ff0SX9f5RjDKcM"
URL1 = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/Web?Query=%27"
URL2 = "%27&$top=50&$format=json"

def geturls(query):
    urls=[]
    r=requests.get(URL1+query+URL2, auth=("", API_KEY))
    for url in r.json()["d"]["results"]:
        urls.append(url["Url"])
    return urls
