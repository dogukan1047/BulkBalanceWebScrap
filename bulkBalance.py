import requests
from bs4 import BeautifulSoup
import pandas as pd


hisseler=["ACSEL"]
# Hisse isimlerini almak için istekte bulunduk
url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=AKSGY"
r=requests.get(url)
# Sayfanın html içeriğini text olarak aldık
s=BeautifulSoup(r.text,"html.parser")

s1=s.find("select",id="ddlAddCompare")
c1=s1.findChild("optgroup").findAll("option")

# Hisselerin Kodunu string ifade biçiminde aldık
# for hCode in c1:
#     hisseler.append(hCode.string)


for i in hisseler:
    hisse=i
 
    tarihler=[]
    yillar=[]
    donemler=[]


    url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse
    r1=requests.get(url1)
    soup=BeautifulSoup(r1.text,"html.parser")
    select=soup.find("select",id="ddlMaliTabloDonem1")
    select2=soup.find("select",id="ddlMaliTabloGroup")
    try:
        children=select.findChildren("option")
        grupOne=select2.find("option")["value"]

        for i in children:
            tarihler.append(i.string.rsplit("/"))

        for j in tarihler:
            yillar.append(j[0])
            donemler.append(j[1])

        if len(tarihler)>=4:
            parameters=(
                ("companyCode",hisse),
                ("exchange","TRY"),
                ("financialGroup",grupOne),
                ("year1",yillar[0]),
                ("period1",donemler[0]),
                ("year2",yillar[1]),
                ("period2",donemler[1]),
                ("year3",yillar[2]),
                ("period3",donemler[2]),
                ("year4",yillar[3]),
                ("period4",donemler[3]),
            )

            url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
            r2=requests.get(url2,params=parameters).json()["value"]
            data=pd.DataFrame.from_dict(r2)
            data.drop(columns=["itemCode","itemDescEng"],inplace=True)
        else:
            continue
    except AttributeError:
        continue

    del tarihler[0:4]
    allData=[data]

    for _ in range(0,int(len(tarihler))+1):
        if len(tarihler)==len(yillar):
            del tarihler[0:4]
        else:
            yillar=[]
            donemler=[]
            for j in tarihler:
                yillar.append(j[0])
                donemler.append(j[1])    

            if len(tarihler)>=4:
                parameters2=(
                    ("companyCode",hisse),
                    ("exchange","TRY"),
                    ("financialGroup",grupOne),
                    ("year1",yillar[0]),
                    ("period1",donemler[0]),
                    ("year2",yillar[1]),
                    ("period2",donemler[1]),
                    ("year3",yillar[2]),
                    ("period3",donemler[2]),
                    ("year4",yillar[3]),
                    ("period4",donemler[3]),
                )

                r3=requests.get(url2,params=parameters2).json()["value"]
                data2=pd.DataFrame.from_dict(r3)
                try:
                    data.drop(columns=["itemCode","itemDescEng","itemDescTr"],inplace=True)
                    allData.append(data2)
                except KeyError:
                    continue 


        data3=pd.concat(allData,axis=1)             
        title=["Bilanco"]

        for i in children:
            title.append(i.string)

        titleDiff=len(title)-len(data3.columns)

        if titleDiff!=0:
            del title[-titleDiff:]    

        data3.columns=title
        data3.set_axis(title,axis=1)
        data3[title[1:]]=data3[title[1:]].astype(float)
        data3.fillna(0,inplace=True)
        data3.to_excel("allData.xlsx",index=False)      
     





   

    

    


 