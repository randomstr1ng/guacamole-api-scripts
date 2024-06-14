#!/usr/bin/env python3

import requests
from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()
def arguments():
    description = "This script allows to add a new RDP connection to Apache Guacamole."
    usage = "%(prog)s [options]"
    parser = ArgumentParser(usage=usage, description=description)
    target = parser.add_argument_group("Target")
    target.add_argument("--guacamole-host","-ghost", dest="GUACAMOLE_HOST", help="IP/Hostname of Apache Guacamole Server", required=True)
    target.add_argument("--guacamole-port","-gport", dest="GUACAMOLE_PORT", help="PORT of Apache Guacamole Server", default="8443")
    target.add_argument("--guacamole-user", "-guser", dest = "GUACAMOLE_USER", help = "Username for Apache Guacamole Server", default = "guacadmin")
    target.add_argument("--guacamole-password", "-gpass", dest="GUACAMOLE_PASSWORD", help="Password for Apache Guacamole Server", required=True)
    target.add_argument("--entry-name", "-n", dest="NAME", help="Name for the Entry", required=True)
    target.add_argument("--host", "-t", dest="HOST", help="IP/Hostname of Entry", required=True)
    target.add_argument("--username", "-u", dest="USERNAME", help="Username used by RDP destination", required=True)
    target.add_argument("--password", "-p", dest="PASSWORD", help="Password used by RDP destination", required=True)
    options = parser.parse_args()
    return options
def get_token(host, port, username, password):
    parameters = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(f"https://{host}:{port}/api/tokens", headers=headers, data=parameters, verify=False)
    token = response.json()["authToken"]
    datasource = response.json()["dataSource"]
    return token, datasource

def add_rdp_connection(host, port, token, datasource, connection_name, hostname, username, password):
    headers = {
        "Content-Type": "application/json",
    }
    parameters = {"name":connection_name,"identifier":"","parentIdentifier":"ROOT","protocol":"rdp","attributes":{"guacd-encryption":"","failover-only":"","weight":"","max-connections":"","guacd-hostname":None,"guacd-port":"","max-connections-per-user":""},"parameters":{"password":password,"hostname":hostname,"security":"any","port":"3389","username":username,"disable-auth":"","ignore-cert":"","gateway-port":"","server-layout":"","timezone":None,"enable-touch":"","console":"","width":"","height":"","dpi":"","color-depth":"","force-lossless":"","resize-method":"","read-only":"","normalize-clipboard":"","disable-copy":"","disable-paste":"","console-audio":"","disable-audio":"","enable-audio-input":"","enable-printing":"","enable-drive":"","disable-download":"","disable-upload":"","create-drive-path":"","enable-wallpaper":"","enable-theming":"","enable-font-smoothing":"","enable-full-window-drag":"","enable-desktop-composition":"","enable-menu-animations":"","disable-bitmap-caching":"","disable-offscreen-caching":"","disable-glyph-caching":"","preconnection-id":"","recording-exclude-output":"","recording-exclude-mouse":"","recording-exclude-touch":"","recording-include-keys":"","create-recording-path":"","enable-sftp":"","sftp-port":"","sftp-server-alive-interval":"","sftp-disable-download":"","sftp-disable-upload":"","wol-send-packet":"","wol-udp-port":"","wol-wait-time":""}}
    response = requests.post(f"https://{host}:{port}/api/session/data/{datasource}/connections?token={token}", headers=headers, json=parameters, verify=False)
    if response.ok:
        print(f"Connection {connection_name} added successfully")
    else:
        print(f"Failed to add connection {connection_name}")
        print(f"Response: {response.text}")

def main():
    options = arguments()
    token, datasource = get_token(host=options.GUACAMOLE_HOST, port=options.GUACAMOLE_PORT, username=options.GUACAMOLE_USER, password=options.GUACAMOLE_PASSWORD)
    add_rdp_connection(host=options.GUACAMOLE_HOST,port=options.GUACAMOLE_PORT, token=token, datasource=datasource, connection_name=options.NAME, hostname=options.HOST, username=options.USERNAME, password=options.PASSWORD)

if __name__ == "__main__":
    main()