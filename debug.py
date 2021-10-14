import pymysql.cursors
import sql
import re
import requests
from bs4 import BeautifulSoup
import datetime
import cgi

print(
'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Stock Farmers</title>
<link href="bitnami.css" media="all" rel="Stylesheet" type="text/css" />
</head>
<body>
<div>
  <div>
    {htmlData}
  </div>
</div>
</body>
</html>
'''.format(htmlData=1))