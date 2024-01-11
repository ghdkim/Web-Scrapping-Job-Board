# Importing Libraries
from bs4 import BeautifulSoup
# Selenium used for accessing websites that block their code. Automating web browsers will remove the "bot" detection.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# the options used so it works on replit

# Initialization a Chrome browser, but you can use a different browser if wanted by changing the code slightly
browser = webdriver.Chrome(options=options)

# Creating a get_page_count function to construct a URL to search the job based on the 'keyword'
def get_page_count(keyword):
    base_url = "https://www.indeed.com/jobs"
    browser.get(f"{base_url}?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    # Pagination to search the jobs on 5 different pages (if there are 5 pages - 5 pages is the max)
    pagination = soup.find("nav", class_="css-98e656 eu4oa1w0")
    # If there are only 1 page, returns 1 (assuming only 1 page of results)
    if pagination == None:
        return 1
    pages_list = pagination.find ("ul", class_="css-1g90gv6 eu4oa1w0")
    pages = pages_list.find_all("li", recursive=False) # recursive= False to remove the last "li" during data scrapping
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count

# Creating extract_indeed_jobs function
def extract_indeed_jobs(keyword):
    # Determine the number of pages to scrape
    pages = get_page_count (keyword)
    print ("Found", pages, "pages")

    results = []

    for page in range(pages): #return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step
        base_url = "https://www.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print("Requesting", final_url)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
        jobs = job_list.find_all("li", recursive=False)  # recursive=False is used to remove any unnecessary "li" code

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one(
                    "h2 a")  # select uses CSS selector for our search --> use different way of searching for an element
                title = anchor["aria-label"]
                link = anchor["href"]
                company = job.find("span", class_="css-1x7z1ps eu4oa1w0")
                location = job.find("div", class_="css-t4u72d eu4oa1w0")
                job_data = {
                    "link": f"https://www.indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title
                }

                for each in job_data:
                    if job_data[each] != None:
                        job_data[each] = job_data[each].replace(",", " ")

                results.append(job_data)
    return results


