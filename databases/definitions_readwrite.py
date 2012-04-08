import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r"/(\w+)", WordHandler)]
		conn = pymongo.Connection("localhost", 27017)
		self.db = conn["definitions"]
		tornado.web.Application.__init__(self, handlers, debug=True)

class WordHandler(tornado.web.RequestHandler):
	def get(self, word):
		coll = self.application.db.words
		word_doc = coll.find_one({"word": word})
		if word_doc:
			del word_doc["_id"]
			self.write(word_doc)
		else:
			self.set_status(404)
	def post(self, word):
		definition = self.get_argument("definition")
		coll = self.application.db.words
		word_doc = coll.find_one({"word": word})
		if word_doc:
			word_doc['definition'] = definition
			coll.save(word_doc)
		else:
			word_doc = {'word': word, 'definition': definition}
			coll.insert(word_doc)
		del word_doc["_id"]
		self.write(word_doc)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
