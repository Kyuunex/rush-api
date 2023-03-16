Important, You need `git` and Python 3.6+ installed.

# Running for testing or debugging purposes
```bash
git clone https://github.com/Kyuunex/rush-api.git -b main
cd rush-api
pip install -r requirements.txt
./test.py
```

# Installation for production use
Type the following in the command line to install the main branch of this software as a pip package  

```bash
python3 -m pip install git+https://github.com/Kyuunex/rush-api.git@main
```  

To install a specific version, replace `main` at the end with the version you want to install from releases.  
Additionally, every release has a command in its description for easy installation of that specific version.  
But for security reasons, using the latest version is always recommended.  
To update from an older version, simply append `--upgrade` to this command.

### Example Apache 2 configuration
```bash
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerAdmin webmaster@your-domain.com
        ServerName rush.your-domain.com
        
        SSLEngine on
        SSLCertificateFile /root/ssl/cloudflare/your-domain.com.pem
        SSLCertificateKeyFile /root/ssl/cloudflare/your-domain.com.key
        
        WSGIScriptAlias / /var/www/rush-api/rushapiloader.wsgi
        
        LogLevel warn
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
</IfModule>
```
### Example wsgi file:
```python
#!/usr/bin/env python3

import os
import sys
import logging

logging.basicConfig(stream=sys.stderr)
os.environ["RUSH_SQLITE_FILE"] = "/var/www/rush-api-db/rush.sqlite3"
# the path above has to be writable

# sys.path.insert(0,"/var/www/rush-api/")

from rushapi import app as application

```
