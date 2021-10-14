#!python
#-*- coding: utf-8 -*-
import codecs
import sql
import sys
import cgi

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sqlvalue = sql.values('all')


print("Content-Type: text/html;")
print()
print('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Stock Farmers</title>
<link href="bitnami.css" media="all" rel="Stylesheet" type="text/css" />
</head>
<body>
<div>
  <div>
    <div>
        <div class="head"><h1><a href="/template.py">STOCK FARMERS</a></h1></div>
    </div>
  </div>
  <div class="menu">
      <div>
        KOSPI 지수: {kospi}
      </div><br>
      <div>
        KOSDAQ 지수: {kosdaq}
      </div><br>
      <div>
        업데이트 시각: {updateTime}
      </div><br>
      <div><a href="/template.py?id=recommand">추천종목만 보기</a></div><br>
      <div>시장종류</div>
          <input type="checkbox">KOSPI
          <input type="checkbox">KOSDAQ<br>
      <div>종목필터</div>
          <select>
            <option value="">-- 전체 --</option>
            <option value="">제약,헬스</option>
            <option value="">전자</option>
            <option value="">엔터</option>
            <option value="">금융</option>
          </select><br>
      <div>테마</div>
          <select>
            <option value="">-- 전체 --</option>
            <option value="">전기차</option>
            <option value="">자율주행</option>
            <option value="">메타버스</option>
            <option value="">인공지능</option>
            <option value="">3D 프린팅</option>
          </select><br>
      <div><input type="submit" value="Submit"></div>
  </div>
  <div class="body">
    <table>
      <tr class="header">
        <td>종목코드</td>
        <td>종목이름</td>
        <td>상장시장</td>
        <td>액면가</td>
        <td>발행량</td>
        <td>EPS</td>
        <td>PER</td>
        <td>EPSXPER</td>
        <td>EPSXPER 예상값</td>
        <td>S-rim</td>
        <td>증권사 목표값</td>
        <td>현재가</td>
        <td>52주 최고가격</td>
        <td>52주 최저가격</td>
      </tr>      
        {sqlvalue}      
    </table>
  </div>
</div>
</body>
</html>
'''.format(sqlvalue=sqlvalue, kospi=sql.index()[0], kosdaq=sql.index()[1], updateTime=sql.index()[2]))






