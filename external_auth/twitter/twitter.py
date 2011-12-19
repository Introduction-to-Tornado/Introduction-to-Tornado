import tornado.web
import tornado.httpserver
import tornado.auth
import tornado.ioloop

class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('access_key')
		oAuthSecret = self.get_secure_cookie('access_secret')
		userID = self.get_secure_cookie('user_id')
		
		if self.get_argument('oauth_token', None):
			self.get_authenticated_user(self.async_callback(self._twitter_on_auth))
			return
		
		elif oAuthToken and oAuthSecret:
			accessToken = {
				'key': oAuthToken,
				'secret': oAuthSecret
			}
			self.twitter_request('/users/show',
				access_token=accessToken,
				user_id=userID,
				callback=self.async_callback(self._twitter_on_user)
			)
			return
		
		self.authorize_redirect()
	
	def _twitter_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Twitter authentication failed')
		
		self.set_secure_cookie('user_id', str(user['id']))
		self.set_secure_cookie('access_key', user['access_token']['key'])
		self.set_secure_cookie('access_secret', user['access_token']['secret'])
		
		self.redirect('/')
	
	def _twitter_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")
		
		self.render('home.html', user=user)

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.render('logout.html')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', TwitterHandler),
			(r'/logout', LogoutHandler)
		]
		
		settings = {
			'twitter_consumer_key': 'cWc3 ... d3yg',
			'twitter_consumer_secret': 'nEoT ... cCXB4',
			'cookie_secret': 'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==',
			'template_path': 'templates',
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
