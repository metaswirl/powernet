'''
Created on 04.05.2013

@author: Peter
'''

def calc_precision(focus,url_facts):
    relevant = 0
    non_relevant = 0
    for url in url_facts.keys():
        facts = url_facts[url]
        rel_facts = 0
        non_rel_facts = 0
        for fact in facts:
            if fact.is_relevant(focus):
                rel_facts+=1
            else:
                non_rel_facts+=1
        if len(facts)>0:
            if rel_facts*1.0/(rel_facts + non_rel_facts)>0:
                relevant+=1
            else:
                non_relevant += 1
        else:
            non_relevant += 1
    if relevant + non_relevant == 0:
        return 0
    return (float(relevant)/(relevant + non_relevant))

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
    if (relevant+non_relevant==0):
        return 0
    return float(relevant)/(relevant + non_relevant)

beta = 2.0
def calc_fmeasure(precision, recall):
    beta2 = beta*beta
    if precision == 0 or recall == 0:
        return 0
    return (1+beta2) * precision * recall / (beta2 * precision + recall)
