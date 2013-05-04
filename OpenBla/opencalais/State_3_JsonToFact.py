'''
Created on 04.05.2013

@author: Peter
'''
import json
class Fact(object):
    
    def __init__(self,factType,factTypeGroup):
        self.pairs = {'type' : factType,'typeGroup' : factTypeGroup}
        self.other_keys = []
    
    def add(self,key,value):
        self.pairs.update({key:value})
    
    
    def __str__(self, *args, **kwargs):
        string = ""
        for key in self.pairs.keys():
            string += "\n%s: %s" %(key,self.pairs[key])
        return string
    
    def toJson(self):
        return json.dumps(self.pairs)
    
    

def openCalaisJsonToFacts(jsonObject,typeGroup):
    facts = []
    for relation in jsonObject:
#             print relation['_type']
        currentAttribute = Fact(relation['_type'],typeGroup)
        for k,v in relation.items():
            if not k.startswith("_"):
                if isinstance(v, unicode):
                    currentAttribute.add(k,v)
                elif isinstance(v, dict):
                    currentAttribute.other_keys+=v.keys()
                    for dict_key in ['name','nationality']:
                        if v.has_key(dict_key):
                            currentAttribute.add(str(k)+"_"+dict_key,v[dict_key])
        facts.append(currentAttribute)
    return facts

            
        