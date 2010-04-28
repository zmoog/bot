#! /usr/bin/env python

from jabberbot_twisted import JabberBot
from httplib2 import Http
from datetime import datetime

try:
  import json # Python 2.6+
except ImportError:
  import simplejson as json

URI_TEMPLATE = 'http://lollypop.arcobaleno.int/addressbook/json/contact/?name=%s'

class DumbBot(JabberBot):
    """
    Jabber/XMPP bot che permette la consultazione della rubrica aziendale.
    """

    def gotMessage(self, jid, msg, resource):
        """
        Callback invocata da Twisted quando viene ricevuto un messaggio dal 
        server Jabber/XMPP.
        """

        try:

            if not msg or msg == 'empty': 
                print 'dropped msg (%s)' % msg
                return
 
            if len(msg) < 2:
                self.sendMessage(jid, 'Dai, fai uno sforzo, scrivi almeno due caratteri.. ;)')
                return


            self.sendMessage(jid, 'Cerco in informazioni su "%s"...' % msg)


            uri = URI_TEMPLATE % msg
            headers, body = Http().request(uri)

            if headers['status'] == '200':

                contacts = json.loads(body)

                response = 'Ho trovato %d occorrenze di %s:\n' % (len(contacts), msg)
   

                for contact in contacts:


                    response += '%s, %s:\n' % (contact['fields']['last_name'], contact['fields']['first_name'])

                    for phone in contact['fields']['phones']:
 
                        # TODO: rimuovere questa pezza temporanea
                        if phone['type'] == 'o': # interno
                            response += "\t * %s : %s\n" % (phone['type__display'], phone['number'][-3:])
                        else:
                            response += "\t * %s : %s\n" % (phone['type__display'], phone['number'])

 

            else:
                response = 'Ooops!'

            print('response: %s' % response)
            print('jid: %s' % jid)

            self.sendMessage(jid, response)

        except Exception:
            print 'Bad dog!'
            self.sendMessage(jid, "Oops! Sono incappato in un problema.. contatta l'Assitenza <assistenza@cooparcobaleno.net>")


if __name__ == '__main__':

    print "DumbBot running, hit Ctrl+C to quit"
    DumbBot("ippo.happy@gmail.com", "secret", servername="talk.google.com").run()
