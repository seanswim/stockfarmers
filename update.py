import pymysql.cursors
import sql
import re
import requests
from bs4 import BeautifulSoup


idcodes = sql.getIdcode()
for sfidcode in idcodes:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
    url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'.format(sfidcode)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    a = soup
    items = a.find_all("tbody")
    try:
        table = items[11].find_all("tr")

        #전년도 EPS
        b = table[18].find_all('td', attrs={'class':'r'})
        try:
            eps = float(b[4].get_text().replace(',',''))
        except:
            eps = 0

        #전년도 PER
        b = table[21].find_all('td', attrs={'class':'r'})
        try:
            per = float(b[4].get_text().replace(',',''))
        except:
            per = 0

        #전년도 EPS*PER
        epsper = eps*per

        #예상 EPS*PER
        c = table[18].find_all('td', attrs={'class':'r'})
        eeps = c[5].get_text().strip()
        d = table[21].find_all('td', attrs={'class':'r'})
        eper = d[5].get_text().strip()
        if eeps == '' and eper =='':
            eeps = 0
            eper = 0
        else:
            eeps = float(eeps.replace(',',''))
            eper = float(eper.replace(',',''))
        eepsper = eeps*eper

        #S-Rim - 자본총계 3년 평균, ROE평균, 자사주 주식량
        e = table[9].find_all('td', attrs={'class':'r'})
        e1 = float(e[2].get_text().strip().replace(',',''))
        e2 = float(e[3].get_text().strip().replace(',',''))
        e3 = float(e[4].get_text().strip().replace(',',''))

        capitalave = (e1+e2+e3)/3

        f = table[17].find_all('td', attrs={'class':'r'})
        f1 = float(f[2].get_text().strip().replace(',',''))
        f2 = float(f[3].get_text().strip().replace(',',''))
        f3 = float(f[4].get_text().strip().replace(',',''))
        roeave = (f1+f2+f3)/3

        g = a.find('div', attrs={'id':'svdMainGrid1'})
        h = g.find_all('td')[11].get_text()
        h1 = re.split('/', h)
        samount = (h1[0].strip().replace(',',''))

        srim = int(capitalave+(capitalave*(roeave-7))/7)
        #증권사 목표주가
        m = a.find('div', attrs={'id':'svdMainGrid9'})
        m1 = m.find_all('td', attrs={'class':'c'})
        try:
            targetP = m1[1].get_text().replace(',','')
        except:
            targetP = 'NULL'
        #종가
        k = g.find_all('td')[0].get_text()
        k1 = re.split('/', k)
        cprice = (k1[0].strip().replace(',',''))
        #52주최고가격
        l = g.find_all('td')[2].get_text()
        l1 = re.split('/', l)
        hprice = (l1[0].strip().replace(',',''))
        #52주최저가격
        lprice = (l1[1].strip().replace(',',''))

    except:
        eps= 'NULL'
        per= 'NULL'
        epsper= 'NULL'
        eepsper= 'NULL'
        srim= 'NULL'
        targetP = 'NULL'
        cprice= 'NULL'
        hprice= 'NULL'
        lprice= 'NULL'

    #데이터베이스 업데이트
    sql.updateValue(sfidcode, eps, per, epsper, eepsper, srim, targetP, cprice, hprice, lprice)
    print(sfidcode+" is done")

