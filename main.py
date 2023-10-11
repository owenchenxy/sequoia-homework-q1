import json
import re
import requests
import yaml
import argparse
import sys

# fill in the lines of repeated messages
def fill_log_entries(log_entries):
    for i in range(len(log_entries)):
        if '--- last message repeated 1 time ---' in log_entries[i]:
            log_entrie_message = ' '.join(log_entries[i-1].split()[3:])
            log_entries[i] = log_entries[i].replace('--- last message repeated 1 time ---', log_entrie_message)
    return log_entries

# get log entries from log file
def get_log_entries(log):
    with open(log, 'r') as f:
        log_entries = []
        datatime_pattern = r'^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).*'
        current_entry = ''
        for line in f:
            match = re.match(datatime_pattern, line)
            if match and not current_entry:
                current_entry = line
            elif match and current_entry:
                log_entries.append(current_entry)
                current_entry = line
            else:
                current_entry = f'{current_entry}{line}'
    # deal with the last line
    log_entries.append(current_entry)
    return fill_log_entries(log_entries)

def parse_device_name(log_entry):
    return log_entry.split()[3]

def parse_process_name(log_entry):
    return log_entry.split()[4].split('[')[0]

def parse_process_id(log_entry):
    return ' '.join(log_entry.split()[4:]).split('[')[1].split(']')[0]

def parse_description(log_entry):
    return ':'.join(log_entry.split(':')[3:]).lstrip()

def parse_time_window(log_entry):
    hour = int(log_entry.split()[2].split(':')[0])
    return f'{hour}:00 - {hour+1}:00'

def format_log_entries(log_entries):
    result = []
    for log_entry in log_entries:
        try:
            device_name = parse_device_name(log_entry)
            process_name = parse_process_name(log_entry)
            process_id = parse_process_id(log_entry)
            description = parse_description(log_entry)
            time_window = parse_time_window(log_entry)
        except:
            print(f'Error: {log_entry}')
            raise
        result.append({
            'device_name': device_name,
            'process_name': process_name,
            'process_id': process_id,
            'description': description,
            'time_window': time_window
        })
    return result

def get_log_entries_count_by_time_window(log_entries):
    result = {}
    for log_entry in log_entries:
        time_window = log_entry['time_window']
        result[time_window] = result.get(time_window, 0) + 1
    return result

def parse_configuration_file(config):
    with open(config, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Analyze log file and send data to server')  
    parser.add_argument('--log-file', '-f', type=str, help='log file path')
    parser.add_argument('--config', '-c', type=str, help='configuration file path', default='config.yaml')
    args = parser.parse_args()
    if not args.log_file:
        print('Error: log file path is required')
        sys.exit(-1)
    
    # parse log server configurations
    log_file = args.log_file
    log_server_config = parse_configuration_file(args.config).get('log_server', {})
    log_server_protocol = log_server_config.get('protocol', 'http')
    log_server_url = log_server_config.get('url', 'localhost')
    log_server_verify = log_server_config.get('verify', True)
    log_server_cert = log_server_config.get('cert_file', '')

    # parse log file
    log_entries = format_log_entries(get_log_entries(log_file))
    data = {
        "logInfo": log_entries,
        "countByTimeWindow": get_log_entries_count_by_time_window(log_entries)
    }
    # send data to log server
    response = requests.post(f'{log_server_protocol}://{log_server_url}', 
                                json=data, 
                                verify=log_server_verify,
                                cert=log_server_cert)
    if response.status_code != 200:
        print(f'Failed to upload {len(log_entries)} log entries to server({log_server_protocol}://{log_server_url})')
        print(f'Error: {response.status_code} {response.text}')
        sys.exit(-1)

    print(f'Success upload {len(log_entries)} log entries to server({log_server_protocol}://{log_server_url})')
    sys.exit(0)

if __name__ == '__main__':
    main()