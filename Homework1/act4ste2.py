import requests
import argparse
from netaddr import *

ENDPOINT = "http://csec.rit.edu"
TIMEOUT = 5

def scanThis(ip):
    proxies = {"http":"http://"+str(ip)}
    try:
        r = requests.get(ENDPOINT, proxies=proxies, timeout=TIMEOUT)
        if(r.status_code==200):
            return str(ip)
        else:
            return(0)
    except requests.exceptions.Timeout:
        return(0)
    except requests.exceptions.RequestException:
        return(0)

def scanThese(start,end):
    facts = []
    for addy in range(start,end):
        yo = scanThis(IPAddress(addy))
        if(yo!=0):
            facts.append(yo)
    return facts


def main():
    parser = argparse.ArgumentParser(description='Scan a range of IPs')
    parser.add_argument("StartIP", help="Start of the IP range to be scanned.")
    parser.add_argument("EndIP", help="End of the IP range to be scanned.")
    args = parser.parse_args()
    
    start = IPAddress(args.StartIP)
    end = IPAddress(args.EndIP)

    for ip in scanThese(start,end):
        print(ip)
    

if __name__ == '__main__':
    main()