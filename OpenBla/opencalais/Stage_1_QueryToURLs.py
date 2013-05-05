import requests

API_KEY = "4HULCyEIHa2khqOeo4o+UtKxe9jzCq7WiwCgBmxl/gY"
URL1 = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27"
URL2 = "%27&Market=%27en-US%27&$top=50&$format=JSON"

def geturls(query):
    
    urls=[]
#     print "query: "+str(query)
    r=requests.get(URL1+query+URL2, auth=("", API_KEY),verify=False)
    for url in r.json()["d"]["results"]:
        urls.append(url["Url"])
    return urls


def processQueries(queries):
    query_urls_pairs = []
    for query in queries:
        urls = geturls(query)
        query_urls_pairs.append((query,urls))
    return query_urls_pairs