#!/usr/bin/env python
"""
Usage:
   websocket_test  [options] <address>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from __future__ import print_function

from gevent.monkey import patch_all
patch_all()

import gevent
import websocket
from docopt import docopt
import logging
import sys


class WebsocketChannel(object):

    def __init__(self, address):
        self.address = address
        self.start_socket_thread()
        self.thread = None

    def start_socket_thread(self):
        self.socket = websocket.WebSocketApp(self.address,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
        self.thread = gevent.spawn(self.socket.run_forever)
        return self.thread

    def put(self, message):
        try:
            self.socket.send(message)
        except BaseException:
            self.thread.kill()
            self.start_socket_thread()

    def on_open(self, ws=None):
        print('on_open')

    def on_message(self, ws=None):
        print('on_message')

    def on_close(self, ws=None):
        print('on_close')
        self.thread.kill()

    def on_error(self, ws=None, error=None):
        print('WebsocketChannel on_error', error)
        self.on_close(ws)
        gevent.sleep(1)
        self.start_socket_thread()



logger = logging.getLogger('util')


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

        client = WebsocketChannel(parsed_args['<address>'])
        gevent.joinall([client.start_socket_thread()])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
