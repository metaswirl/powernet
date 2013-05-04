#!/usr/bin/python
'''
Description: Websocket server
Author: Niklas Semmler
'''
import sys
import tornado
import tornado.websocket as websocket
from tornado import web, ioloop, httpserver

class MyWebSocketHandler(websocket.WebSocketHandler):
    def initialize(self):
        """ Store the overlay_id this listener is currently viewing.
        Used when updating."""
        self.accessor = accessor

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self, *args, **kwargs):
        print "Client connected from %s" % self.request.remote_ip
        self.application.socket_listeners.add(self) 

        try:
            self.application.echo_server.add_event_listener(self)
        except AttributeError:
            pass # no echo server
        try:
            self.application.pc.add_event_listener(self)
        except AttributeError:
            pass # no RabbitMQ server
        #pika.log.info("WebSocket opened")

    def on_close(self):
        #pika.log.info("WebSocket closed")
        self.application.socket_listeners.remove(self) 
        print "Client disconnected from %s" % self.request.remote_ip
        try:
            self.application.pc.remove_event_listener(self)
        except AttributeError:
            pass # no RabbitMQ server
        try:
            self.application.echo_server.remove_event_listener(self)
        except AttributeError:
            pass # no echo_server

    def on_message(self, message):
        #TODO: look if can map request type here... - or even from the application ws/ mapping
        #self.application.pc.send_message(message) # TODO: do we need to pass it on to rmq?
        if "overlay_id" in message:
            _, overlay_id = message.split("=") #TODO: form JSON on client side, use loads here
            self.overlay_id = overlay_id
            self.update_overlay()
        elif "overlay_list" in message:
            body = json.dumps({'overlay_list': self.ank_accessor.overlays()})
            self.write_message(body)
        elif "ip_allocations" in message:
            body = json.dumps({'ip_allocations': self.ank_accessor.ip_allocations()})
            self.write_message(body)

    def update_overlay(self):
        body = self.ank_accessor[self.overlay_id]
        self.write_message(body)
# and update overlay dropdown
        body = json.dumps({'overlay_list': self.ank_accessor.overlays()})
        self.write_message(body)
#TODO: tidy up the passing of IP allocations

    def update_ip_allocation(self):
        body = json.dumps({'ip_allocations': self.ank_accessor.ip_allocations()})
        self.write_message(body)

class MyRequestHandler(web.RequestHandler):
    def get(self):
        self.write("Searching %s!" % self.get_argument('query'))

def main():
    settings = {
        "static_path": "www/",
        'debug': False,
    }

    accessor = None

    application = web.Application([
        (r'/ws', MyWebSocketHandler, {"accessor": accessor}),
        ("/search", MyRequestHandler),
        ("/(.*)", web.StaticFileHandler, {"path":settings['static_path'], "default_filename":"index.html"} ),
        ], **settings)

    io_loop = ioloop.IOLoop.instance()

    application.listen(8080)
    io_loop.start()

#application.socket_listeners = set() # TODO: see if tornado provides access to listeners

if __name__ == "__main__":
    main()
