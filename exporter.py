import csv
from flask import send_file

def save(jobs): 
  with open("jobs.csv", 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["Source", "Company", "Title", "Keywords", "Listed", "Link"])
      for job in jobs:
        writer.writerow(list(job.values()))
  return

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer= csv.writer(file)
  writer.writerow(["Source", "Company", "Title", "Keywords", "Listed", "Link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return