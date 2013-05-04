'''
Created on 04.05.2013

@author: Peter
'''

import Stage_1_QueryToURLs
import Stage_2_OpenCalais
import Stage_3_Evaluation
import Fact


def getFocusQueries(focus):
    return ["Kim Jong Un"]#,"North Korea leader", "Kim Jong USA"]

    
    
stop_words=["","a","an","of","the","in","at","and","or","by","not","he","she","is","of"]
def remove_stop_words(exacts):
    exactArrs=[]
    for exact in exacts:
        exactArr = exact.split(" ")
        for stop in stop_words:
            if stop in exactArr:
                exactArr.remove(stop)
        exactArrs.append(" ".join(exactArr))
    
    return f7(exactArrs)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def buildqueries(old_queries_score,simpleTexts):
    return simpleTexts

def process(focus):
    c = 0
    queries = getFocusQueries(focus)
    while (c < 5):
        c+=1
        query_urls_pairs = Stage_1_QueryToURLs.processQueries(queries)
        query_fmeasures = {}
        url_fmeasures = {}
        url_scores = {}
        url_facts_big = {}
        rel_exacts_focus = []
        for query,urls in query_urls_pairs:
            url_facts_exacts = Stage_2_OpenCalais.processURLs(urls)
            for url in url_facts_exacts.keys():
                url_facts_big[url]=url_facts_exacts[url][0]
            precision,rel_exacts = Stage_3_Evaluation.calc_precision(focus,url_facts_exacts)
            rel_exacts_focus+=rel_exacts
            recall = Stage_3_Evaluation.calc_recall(focus,url_facts_exacts)
            fMeasure = Stage_3_Evaluation.calc_fmeasure(precision,recall)
            query_fmeasures[query] = fMeasure
            for url in urls:
                if url_fmeasures.has_key(url):
                    url_fmeasures[url].append(fMeasure)
                else:
                    url_fmeasures[url] = [fMeasure]
        for url in url_fmeasures.keys():
            fmeasures = url_fmeasures[url]
            url_scores[url] = sum(fmeasures)
        print url_scores
        simpleTexts = remove_stop_words(rel_exacts_focus)
        queries = buildqueries(query_fmeasures,simpleTexts)

if __name__ == '__main__':
    fact = Fact.Fact()
    fact.add('typeGroup', 'relations')
    fact.add('*', 'Kim Jong Un')
    print fact
    process(fact)
            