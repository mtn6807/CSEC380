import requests

def main():
    r = requests.get('http://csec.rit.edu')
    print(r)

if __name__ == '__main__':
    main()