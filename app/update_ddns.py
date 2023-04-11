#!/usr/bin/env python3

import json
import os
import requests
import sys
import time
from datetime import datetime

IP_API = 'https://api.ipify.org?format=json'
USE_PUBLIC_IP=True
CURRENT_IP_FILE="current_ip.txt"


def print_ts(message):
    dt = datetime.now()
    str_date_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    print('[' + str_date_time + "] " + message)

def get_public_ip():
    print_ts("Getting current Public IP Address...")
    try:
        resp = requests.get(IP_API)
    except requests.ConnectionError as err:
        print_ts(str(err))
        sys.exit(1)
    
    print_ts('Public IP address ' + resp.json()['ip'])
    return resp.json()['ip']

def get_old_ip(ip_addr):
    if not os.path.exists(CURRENT_IP_FILE):
        open(CURRENT_IP_FILE, "w").close
        return None
    
    with open(CURRENT_IP_FILE, "r") as file:
        content = file.read()

        if content == "":
            return None
        else:
            return content

def get_records():
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(os.environ['ZONE_ID']),
        headers={
            'X-Auth-Key':   os.environ['API_KEY'],
            'X-Auth-Email': os.environ['EMAIL']
        })
    print_ts(json.dumps(resp.json(), indent=4, sort_keys=True))
    print_ts('Please find the DNS record ID you would like to update and entry the value into the script')
    sys.exit(0)
        
def save_current_ip(ip_addr):
    with open(CURRENT_IP_FILE, "w") as file:
        file.write(ip_addr)

def wait_ttl():
    print_ts('Waiting ' + os.environ['TTL'] + ' seconds...')
    time.sleep(int(os.environ['TTL']))
    print()


########
# MAIN #
########

while True:
    if USE_PUBLIC_IP:
        ip_addr = get_public_ip()
    else:
        ip_addr = os.environ['IP_ADDRESS']

    old_ip = get_old_ip(ip_addr)
    
    if old_ip == ip_addr:
        print_ts("Current IP (" + ip_addr + ") hasn't changed (" + old_ip + ").")
        wait_ttl()
        continue

    if old_ip is None:
        print_ts("Can't get old IP information.")

    if 'RECORD_ID' not in os.environ:
        get_records()

    resp = requests.put(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            os.environ['ZONE_ID'], os.environ['RECORD_ID']),
        json={
            'type':    'A',
            'name':    os.environ['HOSTNAME'],
            'content': ip_addr,
            'proxied': False
        },
        headers={
            'X-Auth-Key':   os.environ['API_KEY'],
            'X-Auth-Email': os.environ['EMAIL']
        })

    try:
        assert resp.status_code == 200
    except AssertionError as err:
        print('HTTP Error ' + str(resp.status_code) + ' while connecting to Cloudflare API. ' + str(resp.status_code))

    print_ts('Updated DNS record for {}'.format(ip_addr, os.environ['HOSTNAME']))
    save_current_ip(ip_addr)    

    wait_ttl()