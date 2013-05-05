#!/usr/bin/python
'''
Description: Websocket server
Author: Niklas Semmler
'''
import sys
import re
import tornado
import tornado.websocket as websocket
from tornado.netutil import TCPServer
from collections import defaultdict
from tornado import web, ioloop, httpserver

#class tcpserv(TCPServer):

class MyWebSocketHandler(websocket.WebSocketHandler):
    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def on_message(self, message):
        pass

    def open(self):
        self.application.socket_listener.add(self)
        facts = parse_file()
        p = ParseFacts(facts)
        parse = p.run()
        self.write_message(parse)

    def on_close(self):
        self.application.socket_listener.remove(self)

class MyRequestHandler(web.RequestHandler):
    def get(self):
        self.render("www/viz3.html")

class ParseFacts(object):
    def __init__(self, facts):
        self.facts = facts

    def _get_count(self):
        count = 0
        while True:
            yield count
            count += 1
        
    def _get_id(self, name, ids, counter):
        if not ids.has_key(name):
            ids[name] = counter.next()
        return ids[name]

    def _is_relevant(self, fact, entities, relations, ids, counter):
        def sort_out(fact):
            delete = [] 
            for k,v in fact.items():
                if k == 'N/A' or v == 'N/A':
                    delete.append(k)
                elif k == 'quote' or k == 'Quotation':
                    delete.append(k)
                elif k == 'type' or k == 'typeGroup':
                    delete.append(k)
            
            for el in delete:
                del(fact[el])

        names = ["person_name", "company_name", "diplomaticentity1_name"]
        for name, group in zip(names, range(1,len(names))):
            if fact.has_key(name):
                rel = self._is_relation(fact, ids, counter, entities)
                if rel:
                    relations.append(rel)
                else:
                    sort_out(fact)
                    fact["name"] = fact[name] 
                    del(fact[name])
                    fact["group"] = group
                    entities[self._get_id(fact["name"], ids, counter)].update(fact)

    def _is_relation(self, fact, ids, counter, entities):
        """
            TODO:
            check for further relations:
                - love / friendship
                - political support
                - company 2 company relation
        """
        relation_type = ["familyrelationtype", "diplomaticentity2_name"]
        if fact.has_key("familyrelationtype") :
            source = self._get_id(fact["person_name"], ids, counter)
            target = self._get_id(fact["person_relative_name"], ids, counter)
            entities[source].update({"name":fact["person_name"], "group":1})
            entities[target].update({"name":fact["person_relative_name"], "group":1})
            return {"source":source, "target":target, "value":1, "type":fact["familyrelationtype"]}
        elif fact.has_key("person_name") and fact.has_key("company_name"):
            source = self._get_id(fact["person_name"], ids, counter)
            target = self._get_id(fact["company_name"], ids, counter)
            entities[source].update({"name":fact["person_name"], "group":1})
            entities[target].update({"name":fact["company_name"], "group":2})
            return {"source":source, "target":target, "value":2}
        elif fact.has_key("diplomaticentity2_name"):
            source = self._get_id(fact["diplomaticentity1_name"], ids, counter)
            target = self._get_id(fact["diplomaticentity2_name"], ids, counter)
            entities[source].update({"name":fact["diplomaticentity1_name"], "group":3})
            entities[target].update({"name":fact["diplomaticentity2_name"], "group":3})
            return {"source":source, "target":target, "value":3} 
        else:
            return None 

    def run(self):
        """ parse facts """

        def format_fact(fact):
            text = "<table>"
            for k,v in sorted(fact.items()):
                if not (k == "name" or k == "group"):
                    k = str(k).replace('_', ' ')
                    text += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (k, v)
            text += "</table>"

            return {"name":fact["name"], "text":text, "group":fact["group"]}
            
        relations = [] 
        entities = defaultdict(dict)

        ids = {}
        counter = self._get_count()
        for fact in self.facts:
            self._is_relevant(fact, entities, relations, ids, counter)

        relations = {v['source']:v for v in relations}.values()
        entities2 = [] 
        for k,v in entities.items():
            entities2.append(format_fact(v))
            
        return {"nodes":entities2, "links":relations}

def parse_file():
    """ parse file if no direct content is available """

    def _parse_string(string):
        """ parse words from string """
        word_list = re.findall(r'\"([^\"]*)\"', string)
        return {word_list[i]:word_list[i+1] for i in range(0, len(word_list), 2)}

    entries = []

    with open("json_example2.txt", "rb") as f:
        for line in f:
            line = line.translate(None, '\n}{')
            if line:
                dicto = _parse_string(line)
                entries.append(dicto)

    return entries


def main():
    settings = {
        "static_path": "www/",
        'debug': False,
    }

    application = web.Application([
        (r'/ws', MyWebSocketHandler),
        ("/viz3.html", MyRequestHandler, ),
        ("/(.*)", web.StaticFileHandler, {"path":settings['static_path'], "default_filename":"index.html"} ),
        ], **settings)

    application.socket_listener = set() 

    io_loop = ioloop.IOLoop.instance()

    application.listen(8080)
    io_loop.start()


#def connection_ready(sock, fd, events):
#    while True:
#        try:
#            connection, address = sock.accept()
#        except socket.error, e:
#            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
#                raise
#            return
#        connection.setblocking(0)
#        handle_connection(connection, address)

if __name__ == "__main__":
    main()
