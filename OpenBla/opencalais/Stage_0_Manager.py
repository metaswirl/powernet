'''
Created on 04.05.2013

@author: Peter
'''

import Stage_1_QueryToURLs
import Stage_2_OpenCalais
import Stage_3_Evaluation as Stage3
import Fact


def getFocusQueries(focus):
    return ["Kim Jong Un"]#,"North Korea leader", "Kim Jong USA"]

    
    
stop_words=["","a","an","of","the","in","at","and","or",
            "by","not","he","she","is","of","his","her"]
def remove_stop_words(exacts):
    print "vorher: %d" %(len(exacts))
    exactArrs=[]
    
    for exact in exacts:
        neu = ""
        for char in exact:
            wert = ord(char)
            if (wert>64 and wert<123) or char==" ":
                neu+=char
        exactArr = neu.split(" ")
        for ex in exactArr:
            if len(ex)<4:
                exactArr.remove(ex)
        for stop in stop_words:
            if stop in exactArr:
                exactArr.remove(stop)
        exactArrs.append(" ".join(exactArr))
    print "eigentlich: " + str(unique(exactArrs))
    print "nachher: %d" %(len(exactArrs))
    return unique(exactArrs)

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [ el for el in seq if el not in seen and not seen_add(el)]


def process(focus):
    c = 1
    queries = getFocusQueries(focus)
    while (c < 4):
        print "Big Round Nr. %d with %d queries" %(c,len(queries)) 
        c+=1
        query_urls_pairs = Stage_1_QueryToURLs.processQueries(queries)
        query_fmeasures = {}
        url_fmeasures = {}
        url_scores = {}
        url_facts_outerloop = {}
        url_incidents_outerloop = {}
        for query,urls in query_urls_pairs:
            url_facts,url_incidents = Stage_2_OpenCalais.processURLsForFactsAndFindings(urls)
            
            for url in url_facts.keys():
                url_facts_outerloop[url]=url_facts[url]
                url_incidents_outerloop[url]=url_incidents[url]
                
                
            precision = Stage3.calc_precision(focus,url_facts)
            recall = Stage3.calc_recall(focus,url_facts)
            fMeasure = Stage3.calc_fmeasure(precision,recall)
            
            query_fmeasures[query] = fMeasure
            
            for url in urls:
                if url_fmeasures.has_key(url):
                    url_fmeasures[url].append(fMeasure)
                else:
                    url_fmeasures[url] = [fMeasure]
        
        for url in url_fmeasures.keys():
            fmeasures = url_fmeasures[url]
            url_scores[url] = sum(fmeasures)
            

        
        all_scored_urls = url_scores.keys()
        topURLs = sorted(all_scored_urls,key=lambda url:url_scores[url])[0:2]
        allIncidents = []
        for url in topURLs:
            if url_incidents.haskey(url):
                incidents = url_incidents[url]
                allIncidents+=incidents
                if len(allIncidents) > 10:
                    break;
        simpleTexts = allIncidents[0:3]
        new_queries = remove_stop_words(simpleTexts)
        
        old_topQueries = sorted(queries,key=lambda query:query_fmeasures[query])[0:1]
        print "new: %d\nold: %d" %(len(new_queries),len(old_topQueries))
        queries = old_topQueries+new_queries

if __name__ == '__main__':
    fact = Fact.Fact()
    fact.add('typeGroup', 'relations')
    fact.add('*', 'Kim Jong Un')
    print fact
    process(fact)
            