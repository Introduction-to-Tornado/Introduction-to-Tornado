#!/usr/bin/python2.7

import time
import oauth2

CONSUMER_KEY = 'qHOnEtah37wSbeRru5ymwg'
CONSUMER_SECRET = 'oYhFzxG20wUykkFsc9ZJBukMuDCQNEzQnQbgAph6M'
ACCESS_KEY = '525295116-VqgFKOCVh3xAuNhFPvF4BTMEQjEdgo35AhcbdN6X'
ACCESS_SECRET = 'aLa6HhoxOxocn55D94iB1GWNAroTO6VOuRIskOy4'


def oauth(url):

	CONSUMER = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
	access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)

	params = {
		'oauth_version': "1.0",
		'oauth_nonce': oauth2.generate_nonce(),
		'oauth_timestamp': int(time.time()),
		'oauth_token': access_token.key,
		'oauth_consumer_key': CONSUMER.key
	}

	req = oauth2.Request(
		method="GET", url=url, parameters=params, is_form_encoded=True)

	req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), CONSUMER, access_token)
	return req.to_header()['Authorization'].encode('utf-8')
