'''
Created on 04.05.2013

@author: Peter
'''

from calais import Calais
import Stage_2a_JsonToFact
import json
import threading
import time
from random import randint
from multiprocessing import Pool

openCalaisKeys = ["944599rdxsxdcrx27u8qkygj","3tva2pe9esxmts2mscuth8dy","m5wmy4dbwpy65h28hnnesckh",
                  "hf2mgf54btc7htkgn2bep9th","gth235ahv4jv686juf5s7bmy","e37bka7n5wmjyufh2hfuvnm6",
                  "j86d2fkbgutmyue3sbfvxhvx","ba68wfrgxvhs2fw96azsf92q","6m6p68u5wa2kpurbr5ce5u38",
                  "wqff45rpb2jwccndfc4qnh6g","fmmm8sz3v6rg5c2y5tkkxnvn","b4nrac3pywjjtb8wnuyj7yd8",
                  "gmsfdhw6wfhnxdjhjcjy27j5"]

def getOpenCalaisResultFromURL(url):
    API_KEY = openCalaisKeys[randint(0,6)]
    calais = Calais(API_KEY, submitter="python-calais demo")
    try:
        result = calais.analyze_url(url)
    except:
        result = None
    return result

def getFactsAndIncidents(url):
    facts = []
    incidents = []
    openCalaisResult = getOpenCalaisResultFromURL(url)
    if openCalaisResult != None:
#         if hasattr(openCalaisResult,"entities"):
#             url_facts[url]+=(Stage_2a_JsonToFact.openCalaisJsonToFacts(openCalaisResult.entities,"entities"))
        if hasattr(openCalaisResult,"relations"):
            facts,exacts = Stage_2a_JsonToFact.openCalaisJsonToFacts(openCalaisResult.relations,"relations")
            facts+=facts
            incidents+=exacts
    return (url,facts,incidents)

def processURLsForFactsAndFindings(urls):
    
#     print "got %d urls for openCalais.." %(len(urls))
    
    pool = Pool(5)
    factFindingArray = pool.map(getFactsAndIncidents,urls)
    pool.terminate()

    pool.join()
    url_facts = {}
    url_incidents = {}
    for url,facts,findings in factFindingArray:
        url_facts.update({url:facts})
        url_incidents.update({url:findings})
    
    return (url_facts,url_incidents)

