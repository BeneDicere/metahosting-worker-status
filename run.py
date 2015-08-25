#!/usr/bin/env python

import argparse
import config_manager
import logging
import signal
from config_manager import get_backend_class
from queue_manager import send_message


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        help="get debug output",
                        action="store_true")
    parser.add_argument("--logstash",
                        help="log everything (in addition) to logstash "
                             ", give host:port")
    parser.add_argument("--envfile",
                        help="provide a file that tells which not-default "
                        "environment variables to use")
    parser.add_argument("--config",
                        help="provide a config file")
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if args.config:
        config_manager._CONFIG_FILE = args.config
    if args.logstash:
        import logstash
        host, port = args.logstash.split(':')
        logger.addHandler(logstash.TCPLogstashHandler(host=host,
                                                      port=int(port),
                                                      version=1))

    config = config_manager.get_configuration('default')
    updater_class = get_backend_class(config, 'updaterbackend')
    updater = updater_class(config=config, send_method=send_message)

    signal.signal(signal.SIGTERM, updater.stop)
    signal.signal(signal.SIGHUP, updater.stop)
    signal.signal(signal.SIGINT, updater.stop)
    updater.start()

if __name__ == "__main__":
    run()
