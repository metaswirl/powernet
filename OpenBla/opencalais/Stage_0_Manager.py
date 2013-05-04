'''
Created on 04.05.2013

@author: Peter
'''

import Stage_1_QueryToURLs
import Stage_2_OpenCalais
import Stage_3_Evaluation


def getFocusQueries(focus):
    return []



def process(focus):
    query_urls_pairs = Stage_1_QueryToURLs.processQueries(getFocusQueries(focus))
    query_fmeasures = {}
    url_fmeasures = {}
    url_scores = {}
    url_facts_big = {}
    for query,urls in query_urls_pairs:
        url_facts = Stage_2_OpenCalais.processURLs(urls)
        url_facts_big.update(url_facts)
        precision = Stage_3_Evaluation.calc_precision(focus,url_facts)
        recall = Stage_3_Evaluation.calc_recall(focus,url_facts)
        fMeasure = Stage_3_Evaluation.calc_fmeasure(precision,recall)
        query_fmeasures[query] = fMeasure
        for url in urls:
            if url_fmeasures.has_key(url):
                url_fmeasures[url].append(fMeasure)
            else:
                url_fmeasures[url] = [fMeasure]
    for url,fmeasures in url_fmeasures:
        url_scores[url] = sum(fmeasures)
            