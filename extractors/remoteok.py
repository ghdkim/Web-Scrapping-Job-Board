# Importing Libaries
from bs4 import BeautifulSoup
from requests import get

def extract_remoteok_jobs(keyword):
    base_url = f"https://remoteok.io/remote-{keyword}-jobs"
    # Make an HTTP GET request to the constructed URL
    # A custom 'User-Agent' named 'Kimchi' set in the headers to simulate a browser request
    request = get(base_url, headers={"User-Agent": "Kimchi"})
    # request.status_code = 200 means that the website is valid and running
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        results = []
        jobs = soup.select("tr[class^='job job-']") # Use attribute starts with selector

        # Extracting Job Details
        for job_tr in jobs:
            job_post = job_tr.find("td", class_="company_and_position")

            if job_post:
                anchor = job_post.find("a")
                link = anchor["href"] if anchor else ""
                title = anchor.find("h2", itemprop="title").get_text() \
                    if anchor and anchor.find("h2", itemprop="title") \
                    else ""
                company = job_post.find("h3", itemprop="name").get_text() \
                    if job_post.find("h3", itemprop="name") \
                    else ""
                location = job_post.find("div", class_="location").get_text() \
                    if job_post.find("div", class_="location") \
                    else ""

                job_data = {
                    "link": f"https://remoteok.com{link}",
                    "company": company.strip(),
                    "location": location.strip(),
                    "position": title.strip()
                }

                for each in job_data:
                    if job_data[each] != None:
                        job_data[each] = job_data[each].replace(",", " ")

                results.append(job_data)

    return results