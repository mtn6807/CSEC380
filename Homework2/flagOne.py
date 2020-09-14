import userAgent as ua
METHOD = "POST"
FILEPATH = "/"
VERSION = "1.1"
URI = "csec380-core.csec.rit.edu"
PORT = 82

def main():
    #make call
    resp = ua.makeReq(METHOD, FILEPATH, VERSION, URI, PORT)
    
    #format response
    resp = ua.parseResp(resp)
    
    #print fromatted response
    print(resp)
    return resp

if __name__ == "__main__":
    main()