#!/usr/bin/env python3

import requests
from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()


def arguments():
    description = "This script allows to the password of your user in Apache Guacamole."
    usage = "%(prog)s [options]"
    parser = ArgumentParser(usage=usage, description=description)
    target = parser.add_argument_group("Target")
    target.add_argument("--guacamole-host","-ghost", dest="GUACAMOLE_HOST", help="IP/Hostname of Apache Guacamole Server", required=True)
    target.add_argument("--guacamole-port","-gport", dest="GUACAMOLE_PORT", help="PORT of Apache Guacamole Server", default="443")
    target.add_argument("--guacamole-user", "-guser", dest = "GUACAMOLE_USER", help = "Username for Apache Guacamole Server", default = "guacadmin")
    target.add_argument("--guacamole-password", "-gpass", dest="GUACAMOLE_PASSWORD", help="Password for Apache Guacamole Server", required=True)
    target.add_argument("--guacamole-new-password", "-new-pass", dest="GUACAMOLE_NEW_PASSWORD",
                        help="New Password", required=True)
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

def change_password(host, port, token, datasource, old_password, new_password):
    headers = {
        "Content-Type": "application/json",
        "Guacamole-Token": token,
    }
    parameters = {
        "oldPassword": old_password,
        "newPassword": new_password
    }
    #proxies = {"https": "http://127.0.0.1:8080"}
    response = requests.put(f"https://{host}:{port}/api/session/data/{datasource}/users/guacadmin/password", headers=headers, json=parameters, verify=False)
    if response.ok:
        print(f"Password changed successfully")
    else:
        print(f"Failed to change password")
        print(f"Response: {response.text}")

def main():
    options = arguments()
    token, datasource = get_token(host=options.GUACAMOLE_HOST, port=options.GUACAMOLE_PORT, username=options.GUACAMOLE_USER, password=options.GUACAMOLE_PASSWORD)
    change_password(host=options.GUACAMOLE_HOST, port=options.GUACAMOLE_PORT, token=token, datasource=datasource, old_password=options.GUACAMOLE_PASSWORD, new_password=options.GUACAMOLE_NEW_PASSWORD)

if __name__ == "__main__":
    main()