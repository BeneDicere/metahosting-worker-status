import pika
import logging
import json
from retrying import retry
import threading


class BlockingPikaManager(object):
    def __init__(self, host, port, user, password, queue=None):
        logging.debug('Initializing Messaging')
        credentials = pika.PlainCredentials(user, password)
        self.parameters = pika.ConnectionParameters(host=host,
                                                    port=port,
                                                    virtual_host='',
                                                    credentials=credentials)
        self.connection = self._get_connection()
        self.channel = self.connection.channel()
        if type(queue) == str:
            self.channel.queue_declare(queue=queue, durable=True)
        elif type(queue) == list:
            for item in queue:
                self.channel.queue_declare(queue=item, durable=True)
        self.thread = threading.Thread(target=self.channel.start_consuming)
        self.thread.setDaemon(True)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def _get_connection(self):
        logging.info('Establishing connection')
        return pika.BlockingConnection(self.parameters)

    def publish(self, routing_key, message):
        logging.debug('Dispatching %s: %s', routing_key, message)
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   body=json.dumps(message),
                                   properties=pika.BasicProperties(
                                       content_type='application/json'))

    def disconnect(self):
        if self.connection.is_open:
            self.connection.close()
