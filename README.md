# Apache Guacamole helper scripts

## Add new RDP entry via API
```bash
$ python3 add-entry.py -h

usage: add-entry.py [options]

This script allows to add a new RDP connection to Apache Guacamole.

optional arguments:
  -h, --help            show this help message and exit

Target:
  --guacamole-host GUACAMOLE_HOST, -ghost GUACAMOLE_HOST
                        IP/Hostname of Apache Guacamole Server
  --guacamole-port GUACAMOLE_PORT, -gport GUACAMOLE_PORT
                        PORT of Apache Guacamole Server
  --guacamole-user GUACAMOLE_USER, -guser GUACAMOLE_USER
                        Username for Apache Guacamole Server
  --guacamole-password GUACAMOLE_PASSWORD, -gpass GUACAMOLE_PASSWORD
                        Password for Apache Guacamole Server
  --entry-name NAME, -n NAME
                        Name for the Entry
  --host HOST, -t HOST  IP/Hostname of Entry
  --username USERNAME, -u USERNAME
                        Username used by RDP destination
  --password PASSWORD, -p PASSWORD
                        Password used by RDP destination
```