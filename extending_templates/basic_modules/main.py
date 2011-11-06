#!/usr/bin/env python
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Sample": SampleModule},
			debug=True,
			autoescape=None
			)
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"index.html",
			samples=[
				{
					"title":"Item 1",
					"description":"Description for item 1"
				},
				{
					"title":"Item 2",
					"description":"Description for item 2"
				},
				{
					"title":"Item 3",
					"description":"Description for item 3"
				}
			]	
		)


class SampleModule(tornado.web.UIModule):
	def render(self, sample):
		return self.render_string(
			"modules/sample.html", 
			sample=sample
		)

	def html_body(self):
		return "<div class=\"addition\"><p>html_body()</p></div>"
	
	def embedded_javascript(self):
		return "document.write(\"<p>embedded_javascript()</p>\")"
	
	def embedded_css(self):
		return ".addition {color: #A1CAF1}"
		
	def css_files(self):
		return "/static/css/sample.css"
	
	def javascript_files(self):
		return "/static/js/sample.js"

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
