import re
import requests
from bs4 import BeautifulSoup
import time

SKILLS = [
          ' Ada ', ' C ', ' Go', ' Java ', ' R ', '.NET', 
          'API', 'AWS', 'Android', 'Assembly', 'Azure', 'Azure', 
          'Bootstrap', 'C#', 'C++', 'COBOL', 'CSS', 'Dart', 'Dash', 
          'Debian', 'Debian', 'Django', 'Excel', 'Flask', 'GraphQL', 'HTML', 
          'Haskell', 'JQuery', 'JavaScript', 'Kotlin', 'Linux', 'Linux', 'Lisp', 
          'MongoDB', 'MySQL', 'NLP', 'NoSQL', 'Node', 'Objective-C', 'Pandas', 
          'Perl','Plotly', 'PostgreSQL', 'PyCharm', 'PySpark', 'PySpark', 
          'Python', 'Pytorch', 'REST', 'React', 'Ruby', 'Rust', 'SQL', 'Snowflake',
          'Spark', 'SwiftScala', 'Tableau', 'Tensorflow', 'Tkinter', 'TypeScript', 
          'Typescript', 'Ubuntu','Unix', 'Windows', 'iOS'
          ]  

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def fetch_job_ids(keywords, session, max_pages=100):
    job_ids = []
    keywords_mod = keywords.replace(' ', '%20').replace(',', '%2C')
    for start in range(0, max_pages, 25):
        url = f'https://www.linkedin.com/jobs/search/?currentJobId=0000000000&f_WT=2&keywords={keywords_mod}&refresh=true&start={start}'
        r = session.get(url, headers=HEADERS)
        doc = BeautifulSoup(r.text, "html.parser")
        box = doc.find_all(
            'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        job_ids += [match.group().replace('jobPosting:', '')
                    for match in re.finditer('jobPosting:\d{10}', str(box))]
        time.sleep(2)  # rate limit our requests to avoid getting banned
    return job_ids

def fetch_descriptions(job_ids, session):
    descriptions = []
    for job_id in job_ids:
        url = f'https://www.linkedin.com/jobs/view/{job_id}/'
        r = session.get(url, headers=HEADERS)
        doc = BeautifulSoup(r.text, "html.parser")
        description = doc.find(
            'div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5')
        if description:
            descriptions.append(description.text)
        time.sleep(2)  # rate limit our requests to avoid getting banned
    return ''.join(descriptions)

def scrape_linkedin(keywords):
    with requests.Session() as session:
        job_ids = fetch_job_ids(keywords, session)
        bigsoup = fetch_descriptions(job_ids, session)
        
    return {skill: bigsoup.count(skill) for skill in SKILLS}

if __name__ == "__main__":
    results = scrape_linkedin("python developer")
    print(results)
