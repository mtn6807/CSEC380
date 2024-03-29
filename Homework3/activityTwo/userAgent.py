import socket
import ssl
import asyncio

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

def recv_all(connection):
    data = []
    while True:
        data.append(connection.recv(2048))
        if not data[-1]:
            return data

def pull_html(resp):
    holder = []
    first = True 
    for x in resp.split('\n\n'):
        if not first:
            holder.append(x)
        first = False
    return "".join(holder)

def formatHeader(response):
    final = []
    stringresponse = ""
    bytestringresponse = b''
    for i in response:
        stringresponse+=i.decode("utf-8",'replace')
        bytestringresponse = bytestringresponse+i
    final.append(stringresponse.split("\r\n\r\n")[0])
    bytestringresponse = bytearray(bytestringresponse)
    bytestringresponse = bytestringresponse[len(final[0])+4:]
    final.append(bytestringresponse)
    return final    

def makeReq(method, filepath, httpversion, host, port, parameters=[]):
    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    if(port==443):
        s = context.wrap_socket(s,server_hostname=host)
    
    #connect to target
    s.connect((host,port))

    #send request
    request = buildReqStr(method, filepath, httpversion, host, parameters)
    #print("==================req===================\n"+request+"\n\n")
    s.send(request.encode("utf-8"))

    #recieve
    response = recv_all(s)
    http_response = formatHeader(response)

    s.shutdown(1)
    s.close()

    return(http_response)
