from status_updater import StatusUpdater

import logging
import requests

class CadvisorStatusUpdater(StatusUpdater):

    def __init__(self, config, messaging):
        super(CadvisorStatusUpdater, self).__init__(config, messaging)
        self.api = '{}{}'.format(
            config['status_endpoint'].replace('tcp', 'http'), '/api/v2.0/')

    def _get(self, subpath):
        try:
            response = requests.get('{}{}'.format(self.api, subpath))
        except Exception as err:
            logging.error('Unable to make request to api  %s', err.message)
            return None
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_cpu_info(self):
        cores = self._get('machine')
        load = self._get('summary')
        if cores and load:
            cores = cores['num_cores']
            load = load['/']['latest_usage']['cpu']
        return {'cores': cores, 'load': load}

    def get_disk_info(self):
        return 0.

    def get_instance_count(self):
        stats = self._get('stats?type=docker&recursive=true')
        if stats:
            return len(stats.keys())
        else:
            return None

    def get_memory_info(self):
        total = self._get('machine')
        used = self._get('summary')
        free = None
        if total and used:
            total = total['memory_capacity']
            used = used['/']['latest_usage']['memory']
            free = total - used
        return {'total': total, 'used': used, 'free': free}
