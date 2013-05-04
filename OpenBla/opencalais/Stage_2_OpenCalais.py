'''
Created on 04.05.2013

@author: Peter
'''

from calais import Calais
import Stage_2a_JsonToFact
import json
import threading
import time
from multiprocessing import Pool

openCalaisKeys = ["944599rdxsxdcrx27u8qkygj","3tva2pe9esxmts2mscuth8dy","m5wmy4dbwpy65h28hnnesckh",
                  "hf2mgf54btc7htkgn2bep9th","gth235ahv4jv686juf5s7bmy","e37bka7n5wmjyufh2hfuvnm6",
                  "j86d2fkbgutmyue3sbfvxhvx","ba68wfrgxvhs2fw96azsf92q","6m6p68u5wa2kpurbr5ce5u38",
                  "wqff45rpb2jwccndfc4qnh6g","fmmm8sz3v6rg5c2y5tkkxnvn","b4nrac3pywjjtb8wnuyj7yd8",
                  "gmsfdhw6wfhnxdjhjcjy27j5"]

def getOpenCalaisResultFromURL(url):
    API_KEY = openCalaisKeys[0]
    calais = Calais(API_KEY, submitter="python-calais demo")
    try:
        result = calais.analyze_url(url)
    except:
        result = None
    return result

def getFacts(url):
    url_facts_exacts = {}
    url_facts_exacts[url] = [[],[]]
    openCalaisResult = getOpenCalaisResultFromURL(url)
    if openCalaisResult != None:
#         if hasattr(openCalaisResult,"entities"):
#             url_facts[url]+=(Stage_2a_JsonToFact.openCalaisJsonToFacts(openCalaisResult.entities,"entities"))
        if hasattr(openCalaisResult,"relations"):
            facts,exacts = Stage_2a_JsonToFact.openCalaisJsonToFacts(openCalaisResult.relations,"relations")
            url_facts_exacts[url][0]+=facts
            url_facts_exacts[url][1]+=exacts
    return url_facts_exacts

def processURLs(urls):
    
    print "got %d urls for openCalais.." %(len(urls))
    
    pool = Pool(6)
    fact_dicts = pool.map(getFacts,urls)
    pool.terminate()

    pool.join()
    url_facts = {}
    for a_dict in fact_dicts:
        url_facts.update(a_dict)
    
    return url_facts

