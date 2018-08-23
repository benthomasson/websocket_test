#!/usr/bin/env python
"""
Usage:
   websocket_test  [options]

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from __future__ import print_function

import gevent
import json
import websocket


class WebsocketChannel(object):

    def __init__(self, address):
        self.address = address
        self.start_socket_thread()

    def start_socket_thread(self):
        self.socket = websocket.WebSocketApp(self.address,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
        self.thread = gevent.spawn(self.socket.run_forever)

    def put(self, message):
        try:
            self.socket.send(message)
        except BaseException:
            self.thread.kill()
            self.start_socket_thread()

    def on_open(self, ws):
        pass

    def on_message(self, ws):
        pass

    def on_close(self, ws):
        self.thread.kill()

    def on_error(self, ws, error):
        print('WebsocketChannel on_error', error)
        self.on_close(ws)
        gevent.sleep(1)
        self.start_socket_thread()


from docopt import docopt
import logging
import sys

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
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
