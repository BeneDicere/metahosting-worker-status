import logging
from config_manager import get_configuration
from queue_manager.rabbit import BlockingPikaManager


manager = dict()


def set_manager(queue=None):
    config = get_configuration('default')
    if 'host' in config and 'port' in config \
            and 'user' in config and 'pass' in config:
        global manager
        manager[queue] = BlockingPikaManager(host=config['host'],
                                             port=int(config['port']),
                                             user=config['user'],
                                             password=config['pass'],
                                             queue=queue)
    else:
        logging.error('Configuration parameters for messaging missing')


def get_manager(queue=None):
    global manager
    if not manager or queue not in manager:
        set_manager(queue=queue)
    return manager[queue]


def send_message(queue, message):
    get_manager(queue=queue).publish(routing_key=queue,
                                     message=message)
