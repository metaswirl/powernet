'''
Created on 04.05.2013

@author: Peter
'''

def calc_precision(focus,url_facts):
    relevant = 0
    non_relevant = 0
    for url in url_facts.keys():
        facts = url_facts[url]
        is_rel = False;
        for fact in facts:
            if fact.is_relevant(focus):
                relevant+=1
                is_rel = True
                break
        if not is_rel:
            non_relevant += 1
    return float(relevant)/(relevant + non_relevant)

def calc_recall(focus,url_facts):
    relevant = 0
    non_relevant = 0
    for url in url_facts.keys():
        facts = url_facts[url]
        for fact in facts:
            if fact.is_relevant(focus):
                relevant+=1
            else:
                non_relevant += 1
    return float(relevant)/(relevant + non_relevant)
beta = 2.0
def calc_fmeasure(precision, recall):
    beta2 = beta*beta
    if precision == 0 or recall == 0:
        return 0
    return (1+beta2) * precision * recall / (beta2 * precision + recall)
