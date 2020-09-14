import userAgent as ua
from urllib.parse import quote
METHOD = "POST"
VERSION = "1.1"
TOKENFILEPATH = "/getSecure"
CREATEACCFILEPATH = "/createAccount"
LOGINFILEPATH = "/login"
USERNAME = "mtn6807"
URI = "csec380-core.csec.rit.edu"
PORT = 82

def main():
    #make call to get token
    resp = ua.makeReq(METHOD, TOKENFILEPATH, VERSION, URI, PORT)

    #pull token
    body = resp.split("'")[1].split("\\r\\n\\r\\n")[1].split('"')[1]
    token = body.split(": ")[1]

    #make a call to create acc
    resp = ua.makeReq(METHOD, CREATEACCFILEPATH, VERSION, URI, PORT,[f"token={token}",f"username={USERNAME}"])

    #pull password
    password = resp.split("password is ")[1].strip("'")

    #login
    resp = ua.makeReq(METHOD, LOGINFILEPATH, VERSION, URI, PORT,[f"token={token}",f"username={USERNAME}",f"password={quote(password, safe='')}"])
    
    #print formatted response
    prettyResp = ua.parseResp(resp)
    print(prettyResp)
    return resp

if __name__ == "__main__":
    main()