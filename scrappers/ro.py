from bs4 import BeautifulSoup
import requests
import os
import re
os.system('clear')

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)




def roScan(term):
  print("Scrapping RemoteOk...")
  url =f"https://remoteok.io/remote-{term}-jobs"
  results = requests.get(url,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
  soup = BeautifulSoup(results.text, 'html.parser')
  soup = soup.find("table",id="jobsboard").find_all("tr",class_="remoteok-original")
  ro_result=[]
  for t in soup:
    tagName = ""
    if t.find("span",class_="closed tooltip-set"):
      continue
    else:
      if t.find("a", class_="companyLink").find("h3"):
        comp = t.find("a", class_="companyLink").find("h3").string
      if t.find("h2", attrs={"itemprop": "title"}):
        title = t.find("h2", attrs={"itemprop": "title"}).string
      if t.find("div",class_="location"):
        loca = deEmojify(t.find("div",class_="location").string)
      if t.find("h2", attrs={"itemprop": "title"}).parent:
        href=t.find("h2", attrs={"itemprop": "title"}).parent.get("href")
        href="https://remoteok.io/"+href
      if t.find("a", class_="no-border tooltip-set"):
        keyTag= t.find_all("div",class_="tag")
        for kt in keyTag:
          keyword = kt.get("class")[1].replace("tag-","")
          tagName +=f"{keyword},"
        try:
          tagName += loca
        except:
          pass
      if t.find("time"):
        listed = deEmojify(t.find("time").get_text(strip=True))
      ro_result.append({"Source":"RemoteOk",  "company":comp,"Title":title,"k":tagName,"listed":listed,"link":href})
  print("RemoteOk: Scrapping Finished")
  print(f"Scrapped {len(ro_result)} jobs")
  return ro_result
  