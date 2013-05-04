'''
Created on 04.05.2013

@author: Peter
'''

def calc_precision(focus,url_facts_exacts):
    relevant = 0
    non_relevant = 0
    rel_exacts = []
    for url in url_facts_exacts.keys():
        facts = url_facts_exacts[url][0]
        is_rel = False
        rel_facts = 0
        non_rel_facts = 0
        for fact in facts:
            if fact.is_relevant(focus):
                rel_facts+=1
                rel_exacts+=url_facts_exacts[url][1]
                is_rel = True
            else:
                non_rel_facts+=1
        if len(facts)>0:
            if rel_facts*1.0/(rel_facts + non_rel_facts)>0:
                relevant+=1
            else:
                non_relevant += 1
        else:
            non_relevant += 1
    return (float(relevant)/(relevant + non_relevant),rel_exacts)

def calc_recall(focus,url_facts_exacts):
    relevant = 0
    non_relevant = 0
    for url in url_facts_exacts.keys():
        facts = url_facts_exacts[url][0]
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
