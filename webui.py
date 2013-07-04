__author__ = 'dfine'

## Poll for wifi SSIDs. If one begins with special header, treat the payload as a base64 encoded magnet link.
## Encode it back to base16 and use the utorrent API to add that magnet link.
## Works on OSX only, using the airport CLI found at
##  /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
## For other OS you'd need to write a different method of listing SSIDs.
# Example infohash:  "67FA82B8959D15B0185B543B42B9B309EF90BE7F"  -- debian ISO

import requests
import re
import time
import os
import base64

port = '8889'
username = 'admin'
password = 'setInClient'
magnet_re = "mae"  #SSID header indicating a maefly message

def b64to16(f):
    raw = base64.b64decode(f)
    return base64.b16encode(raw)
def b16to64(f):
    raw = base64.b16decode(f)
    return base64.b64encode(raw)
def EncodeSSID(magnet):
    b64 = b16to64(magnet)
    #return u"\u03BC" + "1-" + b64[0:-4]  ## Maybe stripping the last 4 is needed in the case of unicode? Test.
    return "mae-" + b64

class utWebAPI:
    def __init__(self,port, username, password):
        self.username = username
        self.password = password
        self.url = "http://localhost:%s/gui/" % port
        self.p = requests.post(self.url + 'token.html', auth = (self.username,self.password), data = {'t':self.timestamp()})
        self.guid = self.p.cookies['GUID']
        self.token = self.p.text[44:-13]  # Should probably use a regular expression, but lazy.
        self.cookies = dict(GUID=self.guid)

    def timestamp(self):
        return str(time.time()).split(".")[0]

    def action(self, actions):
        print actions
        args = {'token':self.token, 't':self.timestamp()}
        params = dict(args.items() + actions.items())
        r = requests.get(self.url, auth=(self.username,self.password), cookies = self.cookies, params = params)
        print "params %s" % params
        return r.text

    def list(self):
        return self.action({'list':'1'})

    def add(self, magnet):
        return self.action({'action':'add-url','s':magnet})

session = utWebAPI(port, username, password)


while 1:   # Make this a thread or something.
    scan = os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s').readlines()
    for line in scan:
        ssid = line.split()[0]
        if re.match(magnet_re, ssid):
            print ssid
            payload = ssid.split('-')[1]
            infohash = b64to16(payload)
            magnetLink = "magnet:?xt=urn:btih:%s" % infohash
            print "magnetLink: %s" % magnetlink
            session.add(magnetLink)
    time.sleep(5)


'''
uTorrent API Usage:
session = utWebAPI(port, username, password)
print session.list()
magnetLink = 'magnet:?xt=urn:btih:335990d615594b9be409ccfeb95864e24ec702c7'
print session.add(magnetLink)
'''
