import tornado.web
from datetime import datetime

class FeedListItem(tornado.web.UIModule):
	def render(self, statusItem):
		return self.render_string('entry.html', item=statusItem, format=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S+0000').strftime('%c'))