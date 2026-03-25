import platform
import ifcfg
import netifaces
from requests import get

def get_local_ip():
    lip = 'unknown'
    if platform.system() == 'Windows':
        ifaces = ifcfg.interfaces()
        for iface in ifaces.values():
            if 'wireless lan adapter wi-fi' in iface['device']:
                lip = iface['inet4'][0]
        return lip
    elif platform.system() == 'Linux':
        return netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    else:
        print("OS unknown")

def get_public_ip():
    return get('https://api.ipify.org').content.decode('utf8')
