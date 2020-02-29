#!/usr/bin/env python
# Ref: https://realpython.com/what-is-pip

import cgi
import http.client

server      = 'www.google.com'
url         = '/'
conn        = http.client.HTTPSConnection(server)
conn.request('GET', url)
response    = conn.getresponse()
content_type= response.getheader('Content-Type')
_, params   = cgi.parse_header(content_type)
encoding    = params.get('charset')
data        = response.read()
text        = data.decode(encoding)

print('Response returned: %s : %s'%(response.status, response.reason))
print('Body:')
print(text)

