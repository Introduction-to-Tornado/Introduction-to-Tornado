import tornado.web
import tornado.httpserver
import tornado.ioloop

class MessageCenter(object):
	callbacks = []
	
	def register(self, callback):
		self.callbacks.append(callback)
	
	def send(self, message):
		for c in self.callbacks:
			c(message)
		self.callbacks = []
	
class ChatHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<html><head>BookChat</head><body><ul><li>chat message</li></ul></body></html>")
	
class MessageHandler(tornado.web.RequestHandler):
	def post(self):
		self.application.messageCenter.send(self.get_argument('m'))
		self.set_status(200)
		self.write('{"success":true}')
	
	@tornado.web.asynchronous
	def get(self):
		self.application.messageCenter.register(self.async_callback(self.on_message))
	
	def on_message(self, message):
		self.write('{"message":"%s"}' % message)
		self.finish()
		
class Application(tornado.web.Application):
	def __init__(self):
		self.messageCenter = MessageCenter()
		
		handlers = [
			(r'/chat', ChatHandler),
			(r'/messages', MessageHandler)
		]
		
		settings = {
			'template_path': 'templates'
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
