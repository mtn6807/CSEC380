import userAgent as ua
import re
from bs4 import BeautifulSoup

METHOD = "GET"
FILEPATH = "/study/computing-security-bs"
VERSION = "1.1"
URI = "www.rit.edu"
PORT = 443


def tableDataText(table):    
    def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row       
    return rows

def prettyPrintTable(table):
    for x in table:
        for y in x:
            print(y,end=',')
        print('')

def pullCourses(alltables):
    allCourses = {}
    for table in alltables:
        for row in table:
            coursetag = row[0]
            is_match = bool(re.match("[A-Z]{4}-[0-9]{3}",coursetag))
            if(is_match):
                if(coursetag not in allCourses.keys()):
                    allCourses[coursetag]=[]
                coursename = row[1].split(":")[0].strip("\\n").split("\\n")[0]
                if(coursename not in allCourses[coursetag]):
                    allCourses[coursetag].append(coursename)
    return allCourses

def cleanData(allCourses):
    for course in allCourses.keys():
        if len(allCourses[course])>1:    
                newnames = []
                for name in allCourses[course]:
                    if "General Education" not in name:
                        newnames.append(name)
                allCourses[course] = newnames
    return allCourses

def writeToCSV(courses):
    f = open("courses.csv", "a")
    csv = ""
    for key in courses.keys():
        currentline = key
        for x in courses[key]:
            currentline+=f",{x}"
        currentline+="\n"
        csv+=currentline
        f.write(currentline)

    f.close()

def main():
    #make call
    resp = ua.makeReq(METHOD, FILEPATH, VERSION, URI, PORT)
    try:
        html_doc = resp[1].decode("utf-8")
    except:
        print("couldn't make htmldoc")
        
    soup = BeautifulSoup(html_doc, 'html.parser')

    alltables = []
    for table in soup.find_all('table'):
       alltables.append(tableDataText(table))
    
    allCourses = cleanData(pullCourses(alltables))
    writeToCSV(allCourses)



if __name__ == "__main__":
    main()