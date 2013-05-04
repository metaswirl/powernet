'''
Created on 04.05.2013

@author: Peter
'''

def calc_precision(focus,url_facts):
    relevant = 0
    non_relevant = 0
    for url,facts in url_facts:
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
    pass

def calc_fmeasure(precision, recall):
    return 0
