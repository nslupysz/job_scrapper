from bs4 import BeautifulSoup
import requests
import os

os.system('clear')


def wwrScan(term):
  print("Scrapping WeWorkRemote...")
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  results = requests.get(url)
  soup = BeautifulSoup(results.text,'html.parser')
  jobSoup = soup.find("article").find("ul").find_all("li")

  wwr_result=[]
  for j in jobSoup[:-1]:
    title=j.find("span",class_="title").string
    href= j.find("a").find_next("a").get("href")
    href="https://weworkremotely.com/"+href
    comp=j.find("span",class_="company").string
    try:
      keyOne = j.find("span",class_="region company").string
    except:
      keyOne = ""
    try:
      keyTwo = j.find("span",class_="title").find_next("span",class_="company").string
    except:
      keyTwo = ""
    key = keyTwo + "," + keyOne
    try:
      listed=j.find("time").string
    except:
      listed="Featured"
    wwr_result.append({"Source":"WeWorkRemotely", "company":comp,"Title":title,"k": key,"listed":listed, "link":href})
  print("WeWorkRemote: Scrapping Finished")
  print(f"Scrapped {len(wwr_result)} jobs")
  return wwr_result