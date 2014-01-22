###############################################################################
##
##  Copyright (C) 2011-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from __future__ import absolute_import

from autobahn.wamp.protocol import WampSession
from autobahn.wamp.broker import Broker
from autobahn.wamp.dealer import Dealer


class MyAppSession(WampSession):

   # def __init__(self, foo = "Foo"):
   #    self.foo = foo

   def onSessionOpen(self, info):
      print "MyAppSession.onSessionOpen", info.me, info.peer

   def onSessionClose(self, reason, message):
      print "MyAppSession.onSessionOpen", reason, message


class MyAppSessionFactory:

   def __init__(self):
      self._broker = Broker()
      self._dealer = Dealer()

   def __call__(self):
      return MyAppSession(self._broker, self._dealer)


def makeSession():
   return MyAppSession()


if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   from autobahn.twisted.websocket import WampWebSocketServerFactory

   log.startLogging(sys.stdout)

   sessionFactory = MyAppSessionFactory()

   transportFactory = WampWebSocketServerFactory(sessionFactory, "ws://localhost:9000", debug = True)
   transportFactory.setProtocolOptions(failByDrop = False)

   reactor.listenTCP(9000, transportFactory)
   reactor.run()
