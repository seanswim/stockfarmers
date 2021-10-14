import pymysql.cursors
import datetime
import requests
from bs4 import BeautifulSoup


def getValue():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='111111',
                                 database='sfdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM list LEFT JOIN finance ON list.sfidcode = finance.sfidcode WHERE eps!='NULL'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

def getRecommand():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='111111',
                                 database='sfdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM list LEFT JOIN finance ON list.sfidcode=finance.sfidcode WHERE (eps!='NULL' AND cprice<lprice) OR (eps!='NULL' AND cprice<srim) OR (eps!='NULL' AND cprice<eepsper)"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

def values(a):
    if a == 'all':
        data = getValue()
    elif a == 'recommand':
        data = getRecommand()
    listStr = ''
    i = 0
    while i < len(data):
        listStr = listStr + '''<tr>
            <td>{idcode}</td>
            <td>{name}</td>
            <td>{market}</td>
            <td>{price}</td>
            <td>{amount}</td>
            <td>{eps}</td>
            <td>{per}</td>
            <td>{epsper}</td>
            <td style="color:blue">{eepsper}</td>
            <td style="color:blue">{srim}</td>
            <td style="color:blue">{targetP}</td>
            <td style="color:red">{cprice}</td>
            <td>{hprice}</td>
            <td>{lprice}</td>
          </tr>'''.format(
            idcode=data[i].get('sfidcode'),
            name=data[i].get('sfkname'),
            market=data[i].get('sfmarket'),
            price=data[i].get('sfprice'),
            amount=data[i].get('sfamount'),
            eps=data[i].get('eps'),
            per=data[i].get('per'),
            epsper=data[i].get('epsper'),
            eepsper=data[i].get('eepsper'),
            srim=data[i].get('srim'),
            targetP=data[i].get('targetP'),
            cprice=data[i].get('cprice'),
            hprice=data[i].get('hprice'),
            lprice=data[i].get('lprice'))


        i += 1
    return listStr

def updateValue(sfidcode, eps, per, epsper, eepsper, srim, targetP, cprice, hprice, lprice):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='111111',
                                 database='sfdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE finance SET \
            eps={eps}, \
            per={per}, \
            epsper={epsper}, \
            eepsper={eepsper},\
            srim={srim},\
            targetP={targetP},\
            cprice={cprice},\
            hprice={hprice},\
            lprice={lprice},\
            date=current_date()\
            WHERE sfidcode='{sfidcode}'".format(sfidcode=sfidcode, eps=eps, per=per, epsper=epsper, eepsper=eepsper, srim=srim, targetP=targetP, cprice=cprice, hprice=hprice, lprice=lprice)
            cursor.execute(sql)
            connection.commit()

def getIdcode():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='111111',
                                 database='sfdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = 'SELECT sfidcode FROM finance'
            cursor.execute(sql)
            ids = cursor.fetchall()
            list = []
            for id in ids:
                list.append(id.get('sfidcode'))
            return list

def index():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
    url = 'https://finance.naver.com/'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all('span', attrs={'class':'num'})
    #KOSPI 지수
    kospi = items[0].get_text()
    #KOSDAQ 지수
    kosdaq = items[1].get_text()
    #업데이트 시각
    updateTime = datetime.datetime.now().date()
    return [kospi,kosdaq,updateTime]