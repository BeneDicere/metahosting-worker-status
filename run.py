#!/usr/bin/env python

import signal

from metahosting.common import argument_parsing, logging_setup
from metahosting.common.config_manager \
    import get_backend_class, get_configuration


def run():
    arguments = argument_parsing()
    logging_setup(arguments=arguments)

    config = get_configuration('default')
    updater_class = get_backend_class(config, 'updaterbackend')
    messaging = get_backend_class(config=config,
                                  key='messagingbackend')

    updater = updater_class(config=config, messaging=messaging)
    signal.signal(signal.SIGTERM, updater.stop)
    signal.signal(signal.SIGHUP, updater.stop)
    signal.signal(signal.SIGINT, updater.stop)
    updater.start()

if __name__ == "__main__":
    run()
