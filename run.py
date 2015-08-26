#!/usr/bin/env python

from metahosting.common import argument_parsing, logging_setup
from metahosting.common.config_manager \
    import get_backend_class, get_configuration
from queue_manager import send_message

import signal


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
