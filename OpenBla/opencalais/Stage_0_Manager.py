'''
Created on 04.05.2013

@author: Peter
'''

import Stage_1_QueryToURLs
import Stage_2_OpenCalais
import Stage_3_Evaluation
import Fact


def getFocusQueries(focus):
    return ["Microsoft hires","Microsoft fires"]



def process(focus):
    query_urls_pairs = Stage_1_QueryToURLs.processQueries(getFocusQueries(focus))
    query_fmeasures = {}
    url_fmeasures = {}
    url_scores = {}
    url_facts_big = {}
    for query,urls in query_urls_pairs:
        url_facts = Stage_2_OpenCalais.processURLs(urls)
        for url in url_facts.keys():
            url_facts_big[url]=url_facts[url]
        precision = Stage_3_Evaluation.calc_precision(focus,url_facts)
        recall = Stage_3_Evaluation.calc_recall(focus,url_facts)
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
    for url in url_facts_big.keys():
        facts = url_facts_big[url]
        for fact in facts:
            print fact.toJson()
if __name__ == '__main__':
    fact = Fact.Fact("PersonCareer","relations")
    print fact
    process(fact)
            