# rush-api
rush-api is a URL shortener, made in Flask.

### Installation
Just install this as a pip package, make an apache conf that looks something like this
```bash
<VirtualHost *:443>
ServerAdmin webmaster@your-domain.com
ServerName rush.your-domain.com

SSLEngine on
SSLCertificateFile /ssl/cloudflare/your-domain.com.pem
SSLCertificateKeyFile /ssl/cloudflare/your-domain.com.key

WSGIScriptAlias / /var/www/rushapi/rushapiloader.wsgi

LogLevel warn
ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```
and make a wsgi file that looks something like this
```python
#!/usr/bin/env python3

import sys
import logging

logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/var/www/rush-api/")

from rushapi import app as application

```
