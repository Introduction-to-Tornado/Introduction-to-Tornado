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
			ui_modules={"Sample": SampleModule},
			debug=True,
			autoescape=None
			)
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"index.html",
			header_text = "Header goes here",
			footer_text = "Footer goes here"
		)


class SampleModule(tornado.web.UIModule):
	def render(self, book):
		return self.render_string(
			"modules/book.html", 
			book=book,
		)

	def html_body(self):
		return "<div class=\"addition\"><p>Hello!</p></div>"
	
	def embedded_javascript(self):
		return "document.write(\"hi again!\")"
	
	def embedded_css(self):
		return ".addition {border: 1px solid #F5F5F5}"
		
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
