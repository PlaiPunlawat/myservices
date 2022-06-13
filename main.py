#Author: Chatchawal Sangkeettrakarn
#Date: September 20,2020.

from fastapi import FastAPI
import uvicorn
import numpy as np
import re
import math
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse

app = FastAPI()

def result(res):
    return {"result":res}

@app.get("/")
async def main():
    return 'Hello World'

@app.get("/test")
async def test():
    return 'Test Tutorial'

@app.get("/add")
async def add(a: int = 0, b: int = 0):
    return a+b

@app.get("/mul")
async def mul(a: int = 0, b: int = 0):
    return a*b

@app.get("/pow")
async def pow(a: int = 0, b: int = 0):
    return math.pow(a,b)


def tonumlist(li):
    ls = li.split(',')
    for i in range(len(ls)):
        ls[i] = float(ls[i])
    return list(ls)

@app.get("/asc")
async def asc(li):
    ls = tonumlist(li)
    ls.sort()
    return ls

@app.get("/desc")
async def desc(li):
    ls = tonumlist(li)
    ls.sort(reverse=True)
    return ls

@app.get("/sum")
async def sum(li):
    ls = tonumlist(li)
    return np.sum(np.array(ls))

@app.get("/avg")
async def avg(li):
    ls = tonumlist(li)
    return np.average(ls)

@app.get("/mean")
async def mean(li):
    ls = tonumlist(li)
    return np.mean(ls)

@app.get("/max")
async def max(li):
    ls = tonumlist(li)
    return np.amax(ls)

@app.get("/min")
async def min(li):
    ls = tonumlist(li)
    return np.amin(ls)

@app.get("/validation-ctzid")
async def validation_ctzid(text):
    if(len(text) != 13):
        return False
    
    sum = 0
    listdata = list(text)
    
    for i in range(12):
        sum+=int(listdata[i])*(13-i)

    d13 = (11-(sum%11))%10
        
    return d13==int(listdata[12])

@app.get("/validation-email")
async def validation_email(text):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex,text):
        return True
    else:
        return False
    
    
@app.get("/google-search",response_class=PlainTextResponse)
def google_search(text):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    url = 'https://www.google.com/search?q=' + str(text)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    t = soup.findAll('div', {'class':"r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break
    
    return(result)

@app.get("/Books")
def Books(author: str = 'H.P. Lovecraft/Stephen King/J.K. Rowling/Arthur Conan Doyle/J. R. R. Tolkien/Andrzej Sapkowski'):
    Book_list = {'Necronomicon': 'H.P. Lovecraft',
             'The Call of Cthulhu and Other Weird Stories': 'H.P. Lovecraft',
             'Hearts in Atlantis': 'Stephen King',
             'Dreamcatcher': 'Stephen King',
             'Salem\'s Lot': 'Stephen King',
             'It': 'Stephen King',
             'Harry Potter and the Philosopher\'s Stone': 'J.K. Rowling',
             'Harry Potter and the Chamber of Secrets': 'J.K. Rowling',
             'Harry Potter and the Prisoner of Azkaban': 'J.K. Rowling',
             'Harry Potter and the Goblet of Fire': 'J.K. Rowling',
             'Harry Potter and the Order of the Phoenix': 'J.K. Rowling',
             'Harry Potter and the Half-Blood Prince': 'J.K. Rowling',
             'Harry Potter and the Deathly Hallows': 'J.K. Rowling',
             'Harry Potter and the Cursed Child, Parts I and II': 'J.K. Rowling',
             'The Hound of the Baskervilles': 'Arthur Conan Doyle',
             'The Adventures of Sherlock Holmes': 'Arthur Conan Doyle',
             'A Study in Scarlet': 'Arthur Conan Doyle',
             'The Sign of Four': 'Arthur Conan Doyle',
             'The Valley of Fear': 'Arthur Conan Doyle',
             'The Return of Sherlock Holmes': 'Arthur Conan Doyle',
             'The Hobbit': 'J. R. R. Tolkien',
             'Fellowship of the Ring': 'J. R. R. Tolkien',
             'The Two Towers': 'J. R. R. Tolkien',
             'The Silmarillion': 'J. R. R. Tolkien',
             'Return of the King': 'J. R. R. Tolkien',
             'Unfinished Tales': 'J. R. R. Tolkien',
             'Blood of Elves': 'Andrzej Sapkowski',
             'Sword of Destiny': 'Andrzej Sapkowski',
             'The Lady of the Lake': 'Andrzej Sapkowski',
             'The Time of Contempt': 'Andrzej Sapkowski',
             'Season of Storms': 'Andrzej Sapkowski',
             'The Tower Of The Swallow': 'Andrzej Sapkowski',
             'Baptism of Fire': 'Andrzej Sapkowski'}
    key_list = list(Book_list.keys())
    val_list = list(Book_list.values())
    index_list = []
    for i in range(len(Book_list)):
        if val_list[i] == author:
            index_list.append(i)
    ans = []
    for i in range(len(index_list)):
        ans.append(key_list[index_list[i]])
    return ans

if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 