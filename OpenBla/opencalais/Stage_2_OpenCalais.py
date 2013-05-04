'''
Created on 04.05.2013

@author: Peter
'''

from calais import Calais
import JsonToPostreSQL
import DBJobs

openCalaisKeys = ["944599rdxsxdcrx27u8qkygj","3tva2pe9esxmts2mscuth8dy","m5wmy4dbwpy65h28hnnesckh",
                  "hf2mgf54btc7htkgn2bep9th","gth235ahv4jv686juf5s7bmy","e37bka7n5wmjyufh2hfuvnm6",
                  "j86d2fkbgutmyue3sbfvxhvx","ba68wfrgxvhs2fw96azsf92q","6m6p68u5wa2kpurbr5ce5u38",
                  "wqff45rpb2jwccndfc4qnh6g","fmmm8sz3v6rg5c2y5tkkxnvn","b4nrac3pywjjtb8wnuyj7yd8",
                  "gmsfdhw6wfhnxdjhjcjy27j5"]

def getOpenCalaisResultFromURL(url):
    API_KEY = openCalaisKeys[0]
    calais = Calais(API_KEY, submitter="python-calais demo")
    result = calais.analyze_url(url)
    return result


def processURLs(urls):
    for url in urls:
        openCalaisResult = getOpenCalaisResultFromURL(url)
        facts = JsonToPostreSQL.openCalaisJsonToFacts(openCalaisResult.entities,"entities")
        facts += JsonToPostreSQL.openCalaisJsonToFacts(openCalaisResult.relations,"relations")
#         DBJobs.processURLandFacts((url,facts))


if __name__ == '__main__':
    url = "http://www.csmonitor.com/World/Asia-Pacific/2013/0502/All-eyes-on-Kim-Jong-un-after-North-Korea-gives-15-years-hard-labor-to-US-citizen"
    
    openCalaisResult = getOpenCalaisResultFromURL(url)
    simpleResult = openCalaisResult.raw_response
    openCalaisResult.print_relations()
    JsonToPostreSQL.openCalaisJsonToPostgreSQL(openCalaisResult.entities,"relations")
#     JsonToPostreSQL.openCalaisJsonToPostgreSQL(openCalaisResult.entities,"entities")
#     print getOpenCalaisResultFromURL("http://www.csmonitor.com/World/Asia-Pacific/2013/0502/All-eyes-on-Kim-Jong-un-after-North-Korea-gives-15-years-hard-labor-to-US-citizen")