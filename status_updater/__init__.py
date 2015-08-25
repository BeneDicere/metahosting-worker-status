from abc import ABCMeta, abstractmethod

import logging
import time
import uuid


class StatusUpdater(object):
    __metaclass__ = ABCMeta
    publishing_interval = 10

    def __init__(self, config, send_method):
        self.config = config
        self.send_method = send_method
        self.uuid = _get_uuid(config)
        self.shutdown = False

    def start(self):
        """
        start sending status information to the queue
        """
        logging.info('Status updater started at %s', str(time.ctime()))
        while not self.shutdown:
            logging.info('Publishing status: %s', self.uuid)
            logging.debug('Publishing stats: %s', str(self.get_stats()))
            self.send_method('status', self.get_stats())
            time.sleep(self.publishing_interval)

    def stop(self, signal, stack):
        """
        try to catch a SIGTERM signal in main thread and stop.
        :param signal:
        :param stack:
        :return:
        """
        logging.info('Status updater stopped with signal %s', signal)
        self.shutdown = True

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
        stats['ts'] = time.time()
        logging.debug('collected statistics = %s', stats)
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
