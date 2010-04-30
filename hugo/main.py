#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
import logging

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class XmppHandler(xmpp_handlers.CommandHandler):

	def unhandled_command(self, message=None):
		logging.debug('got unhandled command: ' + message.body)
		message.reply("Doh! Try with /askme")
	
	def askme_command(self, message=None):
		logging.debug('got: ' + message.body)
		message.reply("Doh!")

	def text_message(self, message=None):
		logging.debug('got a text message from ' + message.sender)
		message.reply("Doh! Try with /askme")

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/_ah/xmpp/message/chat/', XmppHandler),
        ],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
