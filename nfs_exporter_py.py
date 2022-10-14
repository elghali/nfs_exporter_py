from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import os, sys, logging
import yaml

dir_path = ['/opt']
scan_subdir = [False]
metric_freq = 10
port = 9469
logging_level= 'DEBUG'

logging.basicConfig(stream=sys.stdout, level=logging_level.upper())
logger = logging.getLogger()

def loadConfig():
    global dir_path, scan_subdir, port, metric_freq, logging_level, logger
    if os.path.exists('./config.yaml'):
        logger.debug('Config file found')
        with open('./config.yaml', 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                #Required configs
                if all(key in config for key in ('dir_path','scan_subdir','port','metric_freq','logging_level')):
                    dir_path = config['dir_path']
                    scan_subdir = config['scan_subdir']
                    port = int(config['port'])
                    metric_freq = int(config['metric_freq'])
                    logging_level = config['logging_level']
                    logger.setLevel(logging_level.upper())
                else:
                    logger.debug('One or more properties are missing from config.yaml, Using default params instead')
                if len(dir_path) != len(scan_subdir):
                    raise Exception('dir_path and scan_dir should have the same number of values, exiting...')
            except yaml.YAMLError as error:
                logger.error('Error while parsing config.yaml', error)
                sys.exit('Fatal Error, Exiting...')
            except Exception as error:
                logger.error(error)
                sys.exit()
    else:
        print('config.yaml does not exist, Using default values')

class FilesNumberCollector(object):
    def __init__(self):
        pass
    def getNumberOfFiles(self, path, scan_subdir):
        if scan_subdir:
            return sum([len(files) for r, d, files in os.walk(path)])
        return len(os.listdir(path))

    def collect(self):
        gauge = GaugeMetricFamily('number_of_files', 'Number of Files in Directory', labels=["dir_path"])
        for index, value in enumerate(dir_path):
            if not os.path.exists(value):
                logger.error('Directory ' + value + ' Does not exists, Skipping')
                continue
            logger.debug('Watching Dir: ' + value + ' scan_subdir ' + str(scan_subdir[index]))
            # Create a metric to track number of files.
            gauge.add_metric([value], self.getNumberOfFiles(value, scan_subdir[index]))
        yield gauge

if __name__ == '__main__':
    # First Load config.yaml file and parse properties
    loadConfig()
    # Start up the server to expose the metrics.
    start_http_server(port)
    REGISTRY.register(FilesNumberCollector())
    # Generate some requests.
    while True:
        #period between collection
        time.sleep(metric_freq)