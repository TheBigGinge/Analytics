import requests
import time
import urllib2


with open('c:/users/ryanm/desktop/input.tsv', 'rb') as ifh:
    start_time = time.time()
    k = ifh.read()
    #print k
    req = urllib2.Request('http://10.17.0.130:8080', k)
    req.add_header('Content-Length', '%d' % len(k))
    req.add_header('Content-Type', 'application/octet-stream')
    res = urllib2.urlopen(req)
    print '=========='
    print res.read()
    print time.time() - start_time
