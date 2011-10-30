#!/usr/bin/env python

import os
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

# define Tornado defaults
define("port", default=8000, help="run on the given port", type=int)

# application configuration
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", SimpleHandler),
			(r"/one/", SimpleHandler),
			(r"/two/", SecondHandler),
			(r"/three/", ThirdHandler),
			(r"/four/", FourthHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		tornado.web.Application.__init__(self, handlers, **settings)

class SimpleHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"simple.html",
			title="Home Page",
			header="Welcome",
			intro="You've landed on my amazing page here."
		)
	
class SecondHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"simple_2.html",
			title="Home Page",
			header="Welcome",
			books=["Learning Python","Programming Collective Intelligence","Restful Web Services"]
		)

class ThirdHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"simple_3.xml",
			title="Home Page",
			header="Welcome",
			books=["Learning Python","Programming Collective Intelligence","Restful Web Services"]
		)
	
	
class FourthHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"simple_4.txt",
			title="Home Page",
			header="Welcome",
			books=["Learning Python","Programming Collective Intelligence","Restful Web Services"]
		)
	

# Start it up
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
