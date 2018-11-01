from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd
import requests


def getPN(prefix, val):
    return prefix + str(val).zfill(4)

def reqHandle(url):
    reqContent = requests.get(url)
    valid  = (reqContent.status_code == 200)
    valid = valid and reqContent.url != "http://www.andymark.com/v/404error-a/404.htm" 
    
    if (valid):
        return bs(reqContent.content, "lxml")
    else:
        return False

def getWeirdVex():
    weirdData = []
    
    for page in weirdVex['URL']:
        itemSoup = reqHandle(page)
        if itemSoup:
            names = itemSoup.find_all("div", class_="name-wrapper")
            pns = itemSoup.find_all("div", class_="sku-wrapper")
            prices = itemSoup.find_all("span", class_="price")
            
            for i in range(0, len(names)):
              partData = {'Part Number': pns[i].string, 'Name': names[i].string, 'Price': prices[i].string, 'URL': page}
              weirdData.append(partData)
    return weirdData

def getVexData():
    
    baseData = []
    prefix = "217-"
    baseURL = "http://www.vexrobotics.com/"
    suffix = ".html"
    
    partVals = list(range(minVal, maxVal))
    partVals += specialVals
    
    for i in tqdm(partVals):
            partNum = getPN(prefix, i)
            url = baseURL + partNum + suffix
            itemSoup = reqHandle(url)
            
            if itemSoup:
                name = itemSoup.find("h1").string
                price = itemSoup.find("span", class_="price").string
                
                partData = {'Part Number': partNum, 'Name': name, 'Price': price, 'URL': url}
                baseData.append(partData)
    return baseData
                    
minVal = 1000
maxVal = 5520
specialVals = [8080, 9090]

oldData = pd.read_excel('2017 Vendor Part Data.xlsx', 'VEX')
weirdVex = pd.read_excel('2017 Vendor Part Data.xlsx', 'Vex Special')

newData = getVexData()
newData += getWeirdVex()