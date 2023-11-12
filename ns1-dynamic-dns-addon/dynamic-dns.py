#!/usr/bin/env python3

from ns1 import NS1, Config
import os
import sys
import requests
import time
import yaml
import json

def load_json_config(config_path):
    """Load config from Home Assistant Add-On"""

    current_config_file = os.path.join(config_path)
    return json.load(open(current_config_file))

def check_ip(record):
    """ Check whether current IP matches IP in DNS
    Arguments:
    record -- the nsone.records.Record object to check
    """
    my_ip = requests.get("https://api.ipify.org/?format=json").json()["ip"]
    dns_ip = record.data['answers'][0]['answer'][0]
    if my_ip == dns_ip:
        log_print("Current IP ({ip}) matches DNS record for {record}"
                  .format(record=record.domain, ip=my_ip))
        return {'matches': True}
    else:
        log_print("Current IP ({my_ip}) does not match DNS record for {record} (record IP={dns_ip})"
                  .format(record=record.domain, my_ip=my_ip, dns_ip=dns_ip))
        return {'matches': False, 'my_ip': my_ip}


def set_ip(record, new_ip):
    """Set record IP address to new_ip"""
    record.update(answers=[str(new_ip)])
    log_print("Allocated new IP {ip} to {record}"
              .format(record=record.domain, ip=new_ip))


def log_print(log_string):
    print(time.strftime("%c") + " ::: " + str(log_string))


def main():

    # Load config from HA addon config
    config = load_json_config('/data/options.json')

    print('Config:')
    print(config)

    if not config['ns1']:
        print('No configuration defined in the add-on, exiting.')
        exit(1)

    config_file = config['ns1']

    for domain in config_file:
        nsone_config = Config()
        nsone_config.createFromAPIKey(domain['api-key'])
        nsone_config["transport"] = "requests"
        client = NS1(config=nsone_config)
        zone = client.loadZone(domain['zone'])

        for record in domain['records-to-update']:
            record = zone.loadRecord(record, 'A')
            result = check_ip(record)
            if result['matches'] is False:
                set_ip(record, result['my_ip'])


if __name__ == "__main__":
    main()
