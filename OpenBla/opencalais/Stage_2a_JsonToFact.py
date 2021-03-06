'''
Created on 04.05.2013

@author: Peter
'''
import json
import Fact
    

def openCalaisJsonToFacts(jsonObject,typeGroup):
    facts = []
    exacts = []
    for relation in jsonObject:
#             print relation['_type']
        currentAttribute = Fact.Fact()
        currentAttribute.add('type',relation['_type'])
        currentAttribute.add('typeGroup',typeGroup)
        for k,v in relation.items():
            if not k.startswith("_"):
                if isinstance(v, unicode):
                    currentAttribute.add(k,v)
                elif isinstance(v, dict):
                    currentAttribute.other_keys+=v.keys()
                    for dict_key in ['name','nationality']:
                        if v.has_key(dict_key):
                            currentAttribute.add(str(k)+"_"+dict_key,v[dict_key])
                elif k=='instances':
                    for instance in v:
                        if instance.has_key("exact"):
                            exacts.append(instance["exact"])
        facts.append(currentAttribute)
    return [facts,exacts]

            
        