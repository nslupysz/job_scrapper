from bs4 import BeautifulSoup
import requests
import os

os.system('clear')

def SOScan(term):
  print("Scraping StackOverflow...")
  url = f"https://stackoverflow.com/jobs?r=true&q={term}"
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  jobSoup = soup.find("div", class_="listResults").find_all("div", class_="grid--cell fl1")
  
  so_result = []
  
  #find if there is more than 1 page
  try:
    pages = soup.find("div", class_= "s-pagination").find_all("span")
    for pg in range(int(pages[-2].string)):
      new_url = f"https://stackoverflow.com/jobs?r=true&q={term}&pg={pg+1}"
      result = requests.get(new_url)
      soup = BeautifulSoup(result.text, "html.parser")
      jobSoup = soup.find("div", class_="listResults").find_all("div", class_="grid--cell fl1")
      for s in jobSoup:
        title = s.find("h2").find("a").string
        href = s.find("h2").find("a").get("href")
        href = "https://stackoverflow.com/" + href
        comp = s.find("h3").find("span").get_text(strip=True)
        key = s.find_all("a",class_="grid--cell s-tag no-tag-menu")
        listed = s.find("ul",class_="mt4 fs-caption fc-black-500 horizontal-list").find("span").string
        keywords = ""
        for k in key:
          keywords += f"{k.string},"
        keywords = keywords[:-1]
        so_result.append({"Source":"StackOverflow",  "company":comp,"Title":title,"k": keywords,"listed":listed,"link":href})
  except:
    for s in jobSoup:
      title = s.find("h2").find("a").string
      href = s.find("h2").find("a").get("href")
      href = "https://stackoverflow.com/" + href
      comp = s.find("h3").find("span").get_text(strip=True)
      key = s.find_all("a",class_="grid--cell s-tag no-tag-menu")
      listed = s.find("ul",class_="mt4 fs-caption fc-black-500 horizontal-list").find("span").string
      keywords = ""
      for k in key:
        keywords += f"{k.string},"
      keywords = keywords[:-1]
      so_result.append({"Source":"StackOverflow", "company":comp,"Title":title,"k": keywords,"listed":listed, "link":href})
  print("StackOverflow: Scrapping Finished")
  print(f"Scrapped {len(so_result)} jobs")
  return so_result