__author__ = 'dfine'


import json
import time
import requests
import base64

url = 'http://localhost:8888/gui/'
secret = "ACJ4HFDSNUFULFQFWJCAPXH64BYAZMCBG" + "AAAAAA="
magnet = "67FA82B8959D15B0185B543B42B9B309EF90BE7F"

def timestamp():
    return str(time.time()).split(".")[0]

def resample64(f):
    raw = base64.b32decode(f)
    return base64.b64encode(raw)

# def resample32(secret):
#    raw = base64.b64decode(secret)
#    return base64.b32encode(raw)

def resample16(f):
    raw = base64.b16decode(f)
    return base64.b64encode(raw)

def generateSSID(f):
    return u"\u03BC" + "1?" + f[0:-4]

def getSession():
    p = requests.post(url + 'token.html', data = {'t':timestamp()})
    guid = p.cookies['GUID']
    token = p.text[44:-13]  # Faster than figuring out how to parse HTML
    return token, guid

def get(payload):
    g = requests.get('http://localhost:8888/gui/', params = payload)
    print g
    return g.text

session = getSession()
print session[1]

test = {'token':session[0],'action':'getsyncfolders','t':timestamp()}
print test
cookies = dict(GUID=session[1])
#print cookies
r = requests.get('http://localhost:8888/gui/', cookies = cookies, params = test)
print r.text














