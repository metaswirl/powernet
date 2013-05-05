#postgresql interface

import psycopg2

class SQLAccess:
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=PowerWeb user=postgres host=ec2-54-242-169-196.compute-1.amazonaws.com password=keineAhnung!")
            self.cur = self.conn.cursor()
        except:
            print "Cant connect to database."
        

    def close(self):
        self.cur.close()
        self.conn.close()

    def give_input(self, text):
        self.cur.execute("SELECT * FROM facts")
        a = self.cur.fetchall()

        fact_list=[]

        for element in a:
            for key in element[1]:
                if "name" in key and text in element[2][element[1].index(key)]:
                    fact_list.append(self.makedict(element[1], element[2]))
        return fact_list

    def makedict(self, keys, values):
        my_dict={}
        for i in xrange(0, len(keys)):
            my_dict[keys[i]] = values[i]
        return my_dict
        
    def save_qfmeasures(self, query_fmeasures, focus):
#         print "insert queryscores"
        for key in query_fmeasures:
#             print "insert key: " + key
            self.cur.execute("SELECT query_insert(%s)", (key,))
            self.cur.execute("SELECT id FROM query WHERE value=%s", (key,))
            query_id = self.cur.fetchall()[0][0]
            keys = focus.pairs.keys()
            values = focus.pairs.values()
            self.cur.execute("SELECT focus_insert(%s, %s)", (keys, values))
            self.cur.execute("SELECT id FROM focus WHERE keys=%s AND values=%s", (keys, values))
            focus_id = self.cur.fetchall()[0][0]
            self.cur.execute("SELECT query_scores_insert(%s, %s, %s)", (query_id, focus_id, query_fmeasures[key]))
        self.conn.commit() 

    def save_urlscores(self, urlscores, focus):
#         print "insert urlscores"
        for key in urlscores:
            self.cur.execute("SELECT url_insert(%s);", (key,))
            self.cur.execute("SELECT id FROM urls WHERE url=%s", (key,))
            url_id = self.cur.fetchall()[0][0]
            keys = focus.pairs.keys()
            values = focus.pairs.values()
            self.cur.execute("SELECT focus_insert(%s, %s)", (keys, values))
            self.cur.execute("SELECT id FROM focus WHERE keys=%s AND values=%s", (keys, values))
            focus_id = self.cur.fetchall()[0][0]
            self.cur.execute("SELECT urls_scores_insert(%s, %s, %s)", (url_id, focus_id, urlscores[key]))
        self.conn.commit()

    def facts_insert(self, facts):
#         print "insert facts: " + str(len(facts))
#         keys = fact.pairs.keys()
#         values = fact.pairs.values()
#         print str(len(keys)) + ":" + str(len(values))
        self.cur.executemany("SELECT facts_insert(%s, %s)",facts)
#         self.cur.execute("SELECT facts_insert(%s, %s)", (keys, values))
        self.conn.commit()
        
        
    