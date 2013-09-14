import urllib
import json
import netifaces

def global_ip_from_jsonip():
	jsonstring = urllib.URLopener().open('http://jsonip.com').read()
	jsonobj = json.loads(jsonstring)
	ip = jsonobj['ip']
	return ip
	
def local_ip():
	ip = netifaces.ifaddresses("wlan0").get(netifaces.AF_INET)[0]['addr']
	return ip
	
def both_ip():
	return {
		'local_ip': local_ip(),
		'global_ip': global_ip_from_jsonip()
	}