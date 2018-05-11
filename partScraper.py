from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

pd.options.mode.chained_assignment = None

amBaseURL = "http://www.andymark.com/product-p/"
wcpBaseURL = "http://www.wcproducts.net/"
vexBaseURL= "http://www.vexrobotics.com/"

xlsx = pd.ExcelFile('Vendor Part Data.xlsx')
amData  = pd.read_excel(xlsx, 'AM')
vexData  = pd.read_excel(xlsx, 'VEX')
wcpData = pd.read_excel(xlsx, 'WCP')
weirdVex = pd.read_excel(xlsx, 'Vex Special')

partData = {}

minVal = 8070
maxVal = 8090

def getWeirdVex():
    global vexData
    
    for page in weirdVex['URL']:
        itemSoup = reqHandle(page)
        if itemSoup:
            names = itemSoup.find_all("div", class_="name-wrapper")
            pns = itemSoup.find_all("div", class_="sku-wrapper")
            prices = itemSoup.find_all("span", class_="price")
            
            for i in range(0, len(names)):
              partData = {'Part Number': pns[i].string, 'Name': names[i].string, 'Price': prices[i].string, 'URL': page}
              newPart = vexData.loc[vexData['Part Number'] == partData['Part Number']].empty
              
              if newPart:
                print(partData)
                vexData = vexData.append(partData, True)

def reqHandle(url):
    reqContent = requests.get(url)
    valid  = (reqContent.status_code == 200)
    valid = valid and reqContent.url != "http://www.andymark.com/v/404error-a/404.htm" 
    
    if (valid):
        return bs(reqContent.content, "lxml")
    else:
        return False

def getPN(prefix, val):
    return prefix + str(val).zfill(4)

def getAmData():
    global amData
    prefix = "am-"
    baseURL = amBaseURL
    suffix = ".htm"
    
    for i in range(minVal, maxVal):
        print "Trying AM for #" + str(i)
        partNum = getPN(prefix, i)
        newPart = amData.loc[amData['Part Number'] == partNum].empty

        if (newPart):
            url = baseURL + partNum + suffix
            itemSoup = reqHandle(url)

            if itemSoup:
                try:
                    print "Adding part " + partNum + "..."
                    name = itemSoup.find("span", {"itemprop" : "name"}).string
                    price = itemSoup.find("span", {"itemprop" : "price"}).string
                    
                    partData = {'Part Number': partNum, 'Name': name, 'Price': price, 'URL': url}
                    amData = amData.append(partData, True)
                except:
                    pass
def getVexData():
    global vexData
    vexData = vexData
    prefix = "217-"
    baseURL = vexBaseURL
    suffix = ".html"
    
    for i in range(minVal, maxVal):
            print "Trying Vex for #" + str(i)
            partNum = getPN(prefix, i)
            newPart = vexData.loc[vexData['Part Number'] == partNum].empty
    
            if (newPart):
                url = baseURL + partNum + suffix
                itemSoup = reqHandle(url)
                
                if itemSoup:
                    print "Adding part " + partNum + "..."
                    name = itemSoup.find("h1").string
                    price = itemSoup.find("span", class_="price").string
                    
                    partData = {'Part Number': partNum, 'Name': name, 'Price': price, 'URL': url}
                    vexData = vexData.append(partData, True)

def getWcpData():
    global wcpData
    prefix1 = "wcp-"
    prefix2 = "WCP-"
    baseURL = wcpBaseURL
    suffix = ""
    
    for i in range(minVal, maxVal):
        print "Trying WCP for #" + str(i)
        partNum = getPN(prefix1, i)
        partNum2 = getPN(prefix2, i)
        
        newPart = wcpData.loc[wcpData['Part Number'] == partNum].empty
        newPart2 = wcpData.loc[wcpData['Part Number'] == partNum2].empty

        if (newPart):
            url = baseURL + partNum + suffix
            itemSoup = reqHandle(url)
            
            if itemSoup:
                print "Adding part " + partNum + "..."
                name = itemSoup.find("h1").string
                price = itemSoup.find("span", class_="price").string
                
                partData = {'Part Number': partNum, 'Name': name, 'Price': price, 'URL': url}
                wcpData = wcpData.append(partData, True)
                
        if (newPart2):
            url = baseURL + partNum2 + suffix
            itemSoup = reqHandle(url)
            
            if itemSoup:
                print "Adding part " + partNum2 + "..."
                name = itemSoup.find("h1").string
                price = itemSoup.find("span", class_="price").string
                
                partData = {'Part Number': partNum2, 'Name': name, 'Price': price, 'URL': url}
                wcpData = wcpData.append(partData, True)
                
def main():
#  getWeirdVex()
#    getWcpData()
#    getVexData()
#    getAmData()
  writer = pd.ExcelWriter('Vendor Part Data.xlsx', engine='xlsxwriter')
  
  amData.to_excel(writer, index=False, sheet_name='AM')
  vexData.to_excel(writer, index=False, sheet_name='VEX')
  wcpData.to_excel(writer, index=False, sheet_name='WCP')
  weirdVex.to_excel(writer, index=False, sheet_name='Vex Special')
  
  for sheet in writer.sheets:
    writer.sheets[sheet].set_column('A:A', 20)
    writer.sheets[sheet].set_column('B:B', 80)
    writer.sheets[sheet].set_column('C:C', 15)
    writer.sheets[sheet].set_column('D:D', 50)
    
  writer.save()
if __name__ == "__main__":
    main()