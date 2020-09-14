import userAgent as ua
METHOD = "POST"
VERSION = "1.1"
TOKENFILEPATH = "/getSecure"
FLAGTHREEFILEPATH = "/getFlag3Challenge"
URI = "csec380-core.csec.rit.edu"
PORT = 82

def solveCaptcha(cap):
    solution = 0
    if("*" in cap):
        cap=cap.split('*')
        solution=int(cap[0])*int(cap[1])
    elif("+" in cap):
        cap=cap.split('+')
        solution=int(cap[0])+int(cap[1])
    elif("-" in cap):
        cap=cap.split('-')
        solution=int(cap[0])-int(cap[1])
    elif("//" in cap):
        cap=cap.split('//')
        solution=int(cap[0])//int(cap[1])
    return solution

def main():
    #make call to get token
    resp = ua.makeReq(METHOD, TOKENFILEPATH, VERSION, URI, PORT)
    
    #pull token
    body = resp.split("'")[1].split("\\r\\n\\r\\n")[1].split('"')[1]
    token = body.split(": ")[1]

    #make a call to get captcha
    resp = ua.makeReq(METHOD, FLAGTHREEFILEPATH, VERSION, URI, PORT,[f"token={token}"])

    #pull captcha
    body = resp.split("'")[1].split("\\r\\n\\r\\n")[1].split('"')[1]
    captcha = body.split(": ")[1]

    #make call to get flag
    resp = ua.makeReq(METHOD, FLAGTHREEFILEPATH, VERSION, URI, PORT,[f"token={token}",f"solution={solveCaptcha(captcha)}"])
    
    #print formatted response
    prettyResp = ua.parseResp(resp)
    print(prettyResp)
    return resp

if __name__ == "__main__":
    main()