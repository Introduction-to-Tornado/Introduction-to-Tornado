#!/usr/bin/env python
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/recommended/", RecommendedHandler),
			(r"/books/([0-9Xx\-]+)", BookHandler),
			(r"/edit/([0-9Xx\-]+)", BookEditHandler),
			(r"/add", BookEditHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Book": BookModule},
			debug=True,
			)
		conn = pymongo.MongoClient("localhost", 27017)
		self.db = conn["bookstore"]
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"index.html",
			page_title = "Burt's Books | Home",
			header_text = "Welcome to Burt's Books!",
		)

class BookHandler(tornado.web.RequestHandler):
	def get(self, isbn=None):
		if isbn:
			coll = self.application.db.books
			book = coll.find_one({"isbn": isbn})
			if book:
				self.render("one_book.html",
					page_title="Burt's Books | " + book['title'],
					header_text=book['title'],
					book=book)
				return
		self.set_header(404)
		return

class BookEditHandler(tornado.web.RequestHandler):
	def get(self, isbn=None):
		book = dict()
		if isbn:
			coll = self.application.db.books
			book = coll.find_one({"isbn": isbn})
		self.render("book_edit.html",
			page_title="Burt's Books",
			header_text="Edit book",
			book=book)

	def post(self, isbn=None):
		import time
		book_fields = ['isbn', 'title', 'subtitle', 'image', 'author',
			'date_released', 'description']
		coll = self.application.db.books
		if isbn:
			book = coll.find_one({"isbn": isbn})
		for key in book_fields:
			book[key] = self.get_argument(key, None)

		if isbn:
			coll.save(book)
		else:
			book['date_added'] = int(time.time())
			coll.insert(book)
		self.redirect("/recommended/")

class RecommendedHandler(tornado.web.RequestHandler):
	def get(self):
		coll = self.application.db.books
		books = coll.find()
		self.render(
			"recommended.html",
			page_title = "Burt's Books | Recommended Reading",
			header_text = "Recommended Reading",
			books = books
		)
		
class BookModule(tornado.web.UIModule):
	def render(self, book):
		return self.render_string(
			"modules/book.html", 
			book=book,
		)
	
	def css_files(self):
		return "css/recommended.css"
	
	def javascript_files(self):
		return "js/recommended.js"


def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
