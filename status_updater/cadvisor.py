import logging
import requests
from status_updater import StatusUpdater


class CadvisorStatusUpdater(StatusUpdater):

    def __init__(self, config, send_method):
        super(CadvisorStatusUpdater, self).__init__(config, send_method)
        self.api = '{}{}'.format(config['status_endpoint'], '/api/v2.0/')

    def _get(self, subpath):
        try:
            response = requests.get('{}{}'.format(self.api, subpath))
        except Exception as err:
            logging.error('Unable to make request to status endpoint %s',
                          err.message)
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
            load = load['/']['minute_usage']['cpu']['mean']
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
            used = used['/']['minute_usage']['memory']['mean']
            free = total - used
        return {'total': total, 'used': used, 'free': free}
