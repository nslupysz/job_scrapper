news =[
  "World",
  "U.S",
  "Politics",
  "Business",
  "Please",
  "STOP",
  "Searching",
  "running out of..spa..ce"
]


from datetime import date
from flask import Flask, render_template, request, send_file, redirect
from scrappers.so import SOScan
from scrappers.wwr import wwrScan
from scrappers.ro import roScan
from exporter import save_to_file

todayDate = date.today()
day = todayDate.strftime("%A")

fakeDB ={}
fakeRecentSearches={}
fakeDBnum={}

app = Flask("Couch Nomads")

def scrape(term):
  aggregate=[]
  aggregate.extend(SOScan(term))
  aggregate.extend(wwrScan(term))
  aggregate.extend(roScan(term))
  fakeDB[term]=aggregate
  fakeDBnum[term]=f"{term.upper()}: {len(fakeDB[term])} jobs"
  return aggregate

def agg_download(down):
  package = []
  for d in down:
    package.extend(fakeDB[d])
  save_to_file(package)
  return 







#SOScan("MAX", "python")

#wwrScan("javascript")
#roScan("python")



@app.route("/")
def home():
  return render_template("home.html", td=todayDate, d = day)

@app.route("/read")
def read():
  try:
    d = request.args.to_dict()
    term =d["job"] 
    if term in fakeDB:
      result = fakeDB[term]
    else:
      result = scrape(term)
    index = int(len(fakeRecentSearches))
    fakeRecentSearches[news[index]] = term
    
    return render_template("read.html", td=todayDate, d = day, result = result, frs=fakeRecentSearches, fdn=fakeDBnum)
  
  except:
    return redirect("/")


@app.route("/recent")
def recent():
  d = request.args.to_dict()
  term =d["job"] 
  result = fakeDB[term]
  return render_template("read.html", td=todayDate, d = day, result = result, frs=fakeRecentSearches,fdn=fakeDBnum)

@app.route("/download")
def down():
  d= request.args.to_dict()
  result = fakeDB
  download=[]
  for key, tod in d.items():
    download.append(key)
  agg_download(download)
  return send_file("jobs.csv", as_attachment=True)


app.run(host="0.0.0.0")
