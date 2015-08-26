#!/usr/bin/env python

import argparse
import logging
import signal
from config_manager import get_backend_class, get_configuration
from queue_manager import send_message


def argument_parsing():
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
    return parser.parse_args()


def logging_setup(arguments):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if arguments.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if arguments.logstash:
        import logstash
        host, port = arguments.logstash.split(':')
        logger.addHandler(logstash.TCPLogstashHandler(host=host,
                                                      port=int(port),
                                                      version=1))


def run():
    arguments = argument_parsing()
    logging_setup(arguments=arguments)

    config = get_configuration('default')
    updater_class = get_backend_class(config, 'updaterbackend')
    updater = updater_class(config=config, send_method=send_message)

    signal.signal(signal.SIGTERM, updater.stop)
    signal.signal(signal.SIGHUP, updater.stop)
    signal.signal(signal.SIGINT, updater.stop)
    updater.start()

if __name__ == "__main__":
    run()
