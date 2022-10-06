from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import os, sys, logging
import yaml

#Basic Logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

#Default Values
dir_path = ['/opt']
metric_freq = 10
port = 9469

class FilesNumberCollector(object):
    def __init__(self):
        pass
    def collect(self):
        gauge = GaugeMetricFamily('number_of_files', 'Number of Files in Directory', labels=["dir_path"])
        for index, value in enumerate(dir_path):
            if not os.path.exists(value):
                logger.error('Directory ' + value + ' Does not exists, Skipping')
                continue
            logger.debug('Watching Dir: ' + value)
            # Create a metric to track number of files.
            gauge.add_metric([value], len(os.listdir(value)))
        yield gauge

if __name__ == '__main__':
    if os.path.exists('./config.yaml'):
        logger.debug('Config file found')
        with open('./config.yaml', 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                dir_path = config['dir_path'].split(',')
                port = int(config['port'])
                metric_freq = int(config['metric_freq'])
            except yaml.YAMLError as error:
                logger.error(error)
    else:
        print('config.yaml does not exist, Using default values')

    # Start up the server to expose the metrics.
    start_http_server(port)
    REGISTRY.register(FilesNumberCollector())
    # Generate some requests.
    while True:
        #period between collection
        time.sleep(metric_freq)