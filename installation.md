# Installation
After making sure you have `git` and Python 3.6+ installed,  
type the following in the command line to install the main branch of software as a pip package  
```bash
python3 -m pip install git+https://github.com/Kyuunex/rush-api.git@main
```  
To install a specific version, replace `main` at the end with the version you want to install from releases.  
Additionally, every release has a command in its description for easy installation of that specific version.  
But it's always recommended using the latest available version for security reasons.  
To update from an older version, simply append `--upgrade` to the your command.

# Running
To run, first export `RUSH_SQLITE_FILE` environment variable with the path to the sqlite3 database for it.
If the sqlite3 database file does not exist at that given path, it will be automatically created.  
After that, you have 2 choices. 
1. To run for testing or debugging purposes, run `test.py`, or copy and paste its contents into the python shell.
2. To run in production as an Apache site, make an Apache conf that looks something like this:
```bash
<VirtualHost *:443>
ServerAdmin webmaster@your-domain.com
ServerName rush.your-domain.com

SSLEngine on
SSLCertificateFile /ssl/cloudflare/your-domain.com.pem
SSLCertificateKeyFile /ssl/cloudflare/your-domain.com.key

WSGIScriptAlias / /var/www/rush-api/rushapiloader.wsgi

LogLevel warn
ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```
After that, make a wsgi file that looks something like this:
```python
#!/usr/bin/env python3

import sys
import logging

logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/var/www/rush-api/")

from rushapi import app as application

```
