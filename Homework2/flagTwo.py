import userAgent as ua
METHOD = "POST"
VERSION = "1.1"
TOKENFILEPATH = "/getSecure"
FLAGTWOFILEPATH = "/getFlag2"
URI = "csec380-core.csec.rit.edu"
PORT = 82

def main():
    #make call to get token
    resp = ua.makeReq(METHOD, TOKENFILEPATH, VERSION, URI, PORT)
    
    prettyResp = ua.parseResp(resp)
    print(prettyResp)

    #pull token
    body = resp.split("'")[1].split("\\r\\n\\r\\n")[1].split('"')[1]
    token = body.split(": ")[1]

    #make a call to get flag
    resp = ua.makeReq(METHOD, FLAGTWOFILEPATH, VERSION, URI, PORT,[f"token={token}"])
    
    #print formatted response
    prettyResp = ua.parseResp(resp)
    print(prettyResp)
    return resp

if __name__ == "__main__":
    main()