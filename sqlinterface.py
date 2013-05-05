#postgresql interface

import psycopg2

class SQLAccess:
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=PowerWeb user=postgres host=ec2-54-242-169-196.compute-1.amazonaws.com password=keineAhnung!")
        except:
            print "Cant connect to database."
        self.cur = self.conn.cursor()

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
        #fact_list+="hier wird peter aufgerufen"
        return fact_list
        #self.conn.commit()

    def makedict(self, keys, values):
        my_dict={}
        for i in xrange(0, len(keys)):
            my_dict[keys[i]] = values[i]
        return my_dict
        
    def save_qfmeasures(self, query_fmeasures, focus):
        for key in query_fmeasures:
            self.cur.execute("SELECT query_insert(%s);", key)
            self.cur.execute("SELECT id FROM query WHERE value=%s", key)
            query_id = self.cur.fetchall()[0][0]
            keys = "{"
            values = "{"
            for key in focus.pairs:
                keys+=key+","
                values+=focus.pairs[key]
            keys = keys[0:-1]+"}"
            values = values[0:-1]+"}"
            self.cur.execute("SELECT focus_insert(%s, %s)", (keys, values))
            self.cur.execute("SELECT id FROM focus WHERE keys=%s AND values=%s", (keys, values))
            focus_id = self.cur.fetchall()[0][0]
            self.cur.execute("SELECT query_scores_insert(%d, %d, %f)", (query_id, focus_id, query_fmeasures[key]))
        self.conn.commit() 

    def save_urlscores(self, urlscores, focus):
        for key in urlscores:
            self.cur.execute("SELECT url_insert(%s);", key)
            self.cur.execute("SELECT id FROM urls WHERE url=%s", key)
            url_id = self.cur.fetchall()[0][0]
            keys = "{"
            values = "{"
            for key in focus.pairs:
                keys+=key+","
                values+=focus.pairs[key]
            keys = keys[0:-1]+"}"
            values = values[0:-1]+"}"
            self.cur.execute("SELECT focus_insert(%s, %s)", (keys, values))
            self.cur.execute("SELECT id FROM focus WHERE keys=%s AND values=%s", (keys, values))
            focus_id = self.cur.fetchall()[0][0]
            self.cur.execute("SELECT urls_scores_insert(%d, %d, %f)", (url_id, focus_id, urlscores[key]))
        self.conn.commit()

    def facts_insert(self, fact):
        keys = "{"
        values = "{"
        for key in fact.pairs:
            keys+=key+","
            values+=fact.pairs[key]
        keys = keys[0:-1]+"}"
        values = values[0:-1]+"}"
        self.cur.execute("SELECT facts_insert(%s, %s)", (keys, values))
        self.conn.commit()
