'''
Created on 04.05.2013

@author: Peter
'''

import json

class Fact(object):
    
    def __init__(self):
        self.pairs = {}
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
    
    def is_relevant(self,focus):
        for key in focus.pairs.keys():
            if key=='*':
                specialVal = focus.pairs['*']
                c = 0
                for selfkey in self.pairs.keys():
                    if self.pairs[selfkey]==specialVal:
                        c+=1
                if c==0:
                    return False
            elif not self.pairs.has_key(key):
                return False
            elif focus.pairs[key] != self.pairs[key]:
                return False;
        return True;
    