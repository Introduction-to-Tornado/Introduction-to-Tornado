import tornado.web
import tornado.httpserver
import tornado.auth
import tornado.ioloop
import tornado.options

import modules

class FacebookHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		accessToken = self.get_secure_cookie('access_token')
		if not accessToken:
			self.redirect('/auth/login')
			return
		
		self.facebook_request(
			"/me/feed",
			access_token=accessToken,
			callback=self.async_callback(self._on_facebook_user_feed))
		
	def _on_facebook_user_feed(self, response):
		name = self.get_secure_cookie('user_name')
		self.render('home.html', feed=response['data'] if response else [], name=name)
	
	@tornado.web.asynchronous
	def post(self):
		accessToken = self.get_secure_cookie('access_token')
		if not accessToken:
			self.redirect('/auth/login')
		
		userInput = self.get_argument('message')
		
		self.facebook_request(
			"/me/feed",
			post_args={'message': userInput},
			access_token=accessToken,
			callback=self.async_callback(self._on_facebook_post_status))
	
	def _on_facebook_post_status(self, response):
		self.redirect('/')

class LoginHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		userID = self.get_secure_cookie('user_id')
		
		if self.get_argument('code', None):
			self.get_authenticated_user(
				redirect_uri='http://example.com/auth/login',
				client_id=self.settings['facebook_api_key'],
				client_secret=self.settings['facebook_secret'],
				code=self.get_argument('code'),
				callback=self.async_callback(self._on_facebook_login))
			return
		elif self.get_secure_cookie('access_token'):
			self.redirect('/')
		
		self.authorize_redirect(
			redirect_uri='http://example.com/auth/login',
			client_id=self.settings['facebook_api_key'],
			extra_params={'scope': 'read_stream,publish_stream'}
		)
	
	def _on_facebook_login(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Facebook authentication failed')
		
		self.set_secure_cookie('user_id', str(user['id']))
		self.set_secure_cookie('user_name', str(user['name']))
		self.set_secure_cookie('access_token', str(user['access_token']))
		self.redirect('/')

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.render('logout.html')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', FacebookHandler),
			(r'/auth/login', LoginHandler),
			(r'/auth/logout',  LogoutHandler)
		]
		
		settings = {
			'facebook_api_key': '2040 ... 8759',
			'facebook_secret': 'eae0 ... 2f08',
			'cookie_secret': 'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==',
			'template_path': 'templates',
			'ui_modules': modules
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
