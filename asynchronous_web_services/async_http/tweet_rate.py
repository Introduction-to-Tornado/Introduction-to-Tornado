#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import base64
import requests
import urllib.parse
import json
import datetime
import time

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

# twitter part

client_key = 'JkX9Hb2EwNsAqeQ7L7TrawslT'
client_secret = 'JlCrckBeq4NQhHBSDwpwBCvbK7f2XlI6qxu2WO2QI9OFXkDYbH'
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type':
                'application/x-www-form-urlencoded;charset=UTF-8'
                }
auth_data = {'grant_type': 'client_credentials'}
auth_resp = requests.post(auth_url, headers=auth_headers,
                          data=auth_data)
access_token = auth_resp.json()['access_token']
search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
search_url = '{}1.1/search/tweets.json?'.format(base_url)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        query = self.get_argument('q')
        search_params = {'q': query, 'result_type': 'recent',
                         'count': 100}

        client = tornado.httpclient.HTTPClient()
        response = client.fetch(search_url +
                                urllib.parse.urlencode(search_params),
                                headers=search_headers)
        body = json.loads(response.body)
        result_count = len(body['statuses'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['statuses'][-1]['created_at']
        oldest_tweet_at = \
            datetime.datetime.strptime(
                raw_oldest_tweet_at,
                '%a %b %d %H:%M:%S +0000 %Y'
                )
        seconds_diff = time.mktime(now.timetuple()) \
            - time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
        <div style="text-align: center">
        <div style="font-size: 72px">%s</div>
        <div style="font-size: 144px">%.02f</div>
        <div style="font-size: 24px">tweets per second</div>
        </div>""" % (query, tweets_per_second))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
