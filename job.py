from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.education.wa.edu.au/current-jobs'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser") 
jobArray = []
site = "https://search.jobs.wa.gov.au/index.php?AdvertID="


for job in content.findAll('article', attrs={'class': 'row job-listing'}):
    if job.find('p', attrs={'class': 'job-sort job-sort__region'}).text != '862' or job.find('p', attrs={"class": 'job-sort job-sort__level'}).text != '22048':
        continue
    jobObject = {
        "id": job.find('p', attrs={"class": "job-sort job-sort__jobid"}).text,
        "date_posted": job.find('p', attrs={"class": "job-sort job-sort__date-posted"}).text,
        "date_close": job.find('p', attrs={"class": "job-sort job-sort__closing-date"}).text,
        "title": job.find("h4", attrs={"class": "job-listing__title"}).text,
        "school": job.find("p", attrs={"class": "job-listing__branch"}).text.strip().replace('\n', '').split(',', 1)[0],
        "url": site + job.find('p', attrs={"class": "job-sort job-sort__jobid"}).text
    }
    jobArray.append(jobObject)

with open('test.json', 'w') as f:
    json.dump(jobArray, f)
    f.close()

with open('test.json', 'r') as f:
    data = json.load(f)

for i in range(len(data)):
    print(data[i]['title'] + ' | ' + data[i]["school"] + ' | ' + data[i]['url'])