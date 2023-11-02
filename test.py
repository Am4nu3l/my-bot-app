from bs4 import BeautifulSoup
import requests as re

response=re.get("https://wikimezmur.org/am/Hana_Tekle/Habte_Semay/Hulun_Besereh").text
soup=BeautifulSoup(response,'lxml')
data = soup.find_all('div')
for h in data:
    c = h.find_all('div', class_='poem')
    if(c):   
        print(c)
    else:
        print("000000")
