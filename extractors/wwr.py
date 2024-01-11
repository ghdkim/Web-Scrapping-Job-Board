# Import Libaries
from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):  # instead of "keyword" replace with = e.g. python, react, java etc.
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        # response.text shows all the html from the webpage
        # require "html.parser" if you are using bs4
        jobs = soup.find_all("section", class_="jobs")
        # class is already reserved by python just like "else, elif and if" so you have to type class_
        # find_all allows you to find all the data within a code

        for job_section in jobs:
            job_posts = job_section.find_all("li")
            job_posts.pop(
                -1)  # the "view-all" code in the html text are always shown at last so therefore use pop(-1) to remove it

            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = (anchor[
                    "href"])  # beautifulsoup already adds in the "dictionary" just like how python can create their own dictionary

                company, kind, location = anchor.find_all("span", class_="company")
                title = anchor.find("span", class_="title")

                # ".string" removes the <span> tags (the html tags)
                job_data = {
                    "link": f"https://weworkremotely.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title.string,
                }
                for each in job_data:
                    if job_data[each] != None:
                        job_data[each] = job_data[each].replace(",", " ") #this whole section is used to replace all the commas in the code with a space
                results.append(job_data)

        # print(len(jobs)) #len = shows the length of the object

        return results

