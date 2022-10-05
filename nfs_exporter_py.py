from prometheus_client import start_http_server, Gauge
import time
import os
import yaml

dir_path = '/opt'
metric_freq = 10
port = 9469

print("First Watching DIR: " + dir_path)
print("First Metric Freq: " + str(metric_freq))

if __name__ == '__main__':
    if os.path.exists('./config.yaml'):
        print('Config file found')
        with open('./config.yaml', 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                dir_path = config['dir_path']
                port = int(config['port'])
                metric_freq = int(config['metric_freq'])
            except yaml.YAMLError as error:
                print(error)
    else:
        print('config.yaml does not exist, Using default values')

    print("Watching DIR: " + dir_path)
    print("Metric Freq: " + str(metric_freq))
    # Create a metric to track number of files.
    NUMBER_FILES = Gauge('number_of_files', 'Number of Files in Directory ' + dir_path)
    NUMBER_FILES.set_function(lambda: len(os.listdir(dir_path)))

    # Start up the server to expose the metrics.
    start_http_server(port)
    # Generate some requests.
    while True:
        #period between collection
        time.sleep(metric_freq)