from abc import ABCMeta, abstractmethod


import logging
import time
import uuid


class StatusUpdater(object):
    __metaclass__ = ABCMeta

    def __init__(self, config, send_method):
        self.config = config
        self.send_method = send_method
        self.uuid = _get_uuid(config)
        self.type = config['type']
        self.running = False

    def start(self):
        """
        start sending status information to the queue
        """
        self.running = True
        logging.info('Status updater started at %s', str(time.ctime()))
        while self.running:
            stats = self.get_stats()
            logging.info('Publishing status: %s', self.uuid)
            logging.debug('Publishing status: %s', str(stats))
            self.send_method('status', stats)
            time.sleep(10)

    def stop(self, signal, stack):
        """
        try to catch a SIGTERM signal in main thread and stop.
        :param signal:
        :param stack:
        :return:
        """
        logging.info('Status updater stopped with signal %s', signal)
        self.running = False

    @abstractmethod
    def get_cpu_info(self):
        pass

    @abstractmethod
    def get_disk_info(self):
        pass

    @abstractmethod
    def get_instance_count(self):
        pass

    @abstractmethod
    def get_memory_info(self):
        pass

    def get_stats(self):
        stats = dict()
        stats['cpu'] = self.get_cpu_info()
        stats['disk'] = self.get_disk_info()
        stats['instances'] = self.get_instance_count()
        stats['memory'] = self.get_memory_info()
        stats['uuid'] = self.uuid
        stats['type'] = self.type
        stats['ts'] = time.time()
        return stats


def _get_uuid(conf):
    content = ''
    try:
        filehandler = open(conf['uuid_source'], 'r')
        content = (filehandler.read()).rstrip()
        return str(uuid.UUID(content))
    except IOError:
        logging.error('Not able to read file: %s ', conf['uuid_source'])
    except ValueError:
        logging.error('Not able to validate uuid: %s ', content)
    except KeyError:
        logging.error('No path for uuid file in conf')
    return str(uuid.uuid4())
