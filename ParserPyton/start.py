import requests
import time
import sys
import pyodbc
import uuid
from bs4 import BeautifulSoup
from ms_sql import ms_sql


globalurl = ""
curpage = 0
sql = ms_sql()
headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
'''
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.100 Safari/537.36
Mozilla/5.0 (X11; U; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.132 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.95 Safari/537.36
'''
def parse_page(url):
    global globalurl
    globalurl = url
    global headers

    page = requests.get(url, headers=headers, verify=False, timeout=30)
    if page.status_code != 200:
        sys.exit("Error! status_code: " + page.status_code)

    #print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    res = soup.find(id ='search-result').find_all('a') #, class_ = 'btn-select-history')

    lotsurl = []

    for link in res:
        href = link.get('href')
        if (href.startswith('https')):
            lotsurl.append(href)

    for lot in lotsurl:
        parse_lot(lot)
    #parse_lot(lotsurl[1])

def parse_lot(loturl):
    #print(loturl)
    global headers
    page = requests.get(loturl, headers=headers, verify=False, timeout=30)
    if page.status_code != 200:
        sys.exit("Error! status_code: " + page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find(class_ = 'table table-bordered table-hover')
    if table is None:
        sys.exit("Error! Capcha")

    trs = table.find_all("tr")
    bin = ""
    thlist = []
    tdlist = []
    for tr in trs:
        th = tr.find("th")
        th_text = th.get_text()
        thlist.append(th_text)
        print(th.get_text())

        td = tr.find("td")
        td_text = get_td(td)
        tdlist.append(td_text)
        print(td_text)

        if th_text == "БИН заказчика":
            bin = td_text

    global sql
    global curpage

    uid = str(uuid.uuid4())

    sql.addlink(loturl, bin, curpage, uid)

    for i in range(len(thlist)):
        sql.addvalues(bin, thlist[i], tdlist[i], uid)

    time.sleep(2)

def get_td(td):
    td_list = []
    for string in td.stripped_strings:
        td_list.append(string)

    if (len(td_list) > 0):
        return td_list[0]
    else:
        return ""

def main():
    global curpage
    url = "https://.kz/ru/search/lots?filter%5Bname%5D=%D1%81%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5&count_record=50&page="
    for i in range(55,56):
        curpage = i
        parse_page(url+str(i))


if __name__ == '__main__':
    main()



