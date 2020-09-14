import socket

def buildBody(param):
    body = ""
    for x in param:
        if body=="":
            body+=f"{x}"
        else:
            body+=f"&{x}"
    return body

def buildReqStr(method, path, version, host, parameters, contentType="application/x-www-form-urlencoded; charset=utf-8", userAgent="Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko"):
    #format checking
    if('/' not in path):
        path = '/'+path
    if('HTTP/' not in version):
        version = 'HTTP/'+version

    #get bodystr
    bodystr=buildBody(parameters)

    #add headers
    reqstr =f"{method} {path} {version}"
    reqstr +=f"\r\nHOST: {host}"
    reqstr +=f"\r\nContent-Type: {contentType}"
    reqstr +=f"\r\nUser-Agent: {userAgent}"
    reqstr +=f"\r\nAccept: text/html"
    reqstr +=f"\r\nAccept-Language: en-US"
    reqstr +=f"\r\nAccept-Encoding: text/html"
    reqstr +=f"\r\nContent-Length: {len(bodystr)}"
    reqstr +=f"\r\n\r\n"
    reqstr +=f"{bodystr}"
    
    return reqstr


def parseResp(res):
    final = ""
    #res = res.split("'")[1]
    for x in res.split("\\r\\n"):
        final+=x
        final+='\n'
    return final


def makeReq(method, filepath, httpversion, host, port, parameters=[]):
    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to target
    s.connect((host,port))

    #send request
    request = buildReqStr(method, filepath, httpversion, host, parameters)
    s.send(request.encode("utf-8"))

    #recieve
    response = s.recv(4096).decode("ascii")
    http_response = repr(response)

    s.shutdown(1)
    s.close()

    #print
    return(http_response)
