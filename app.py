# Import and Initial Setup
from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.file import save_to_file
from extractors.remoteok import extract_remoteok_jobs

# Flask Application Initialization
app = Flask(__name__)

# Database Initialization
db = {}

# Routes and Views
# When a user visits the root URL, the home function renders home.html.
@app.route("/")
def home():  # put application's code here
    return render_template("home.html")

# This route handles the search functionality.
@app.route("/search")
def search():
    # It captures the keyword from the request arguments.
    keyword = request.args.get("keyword") #args = argument to grab the search results from html code
    # If keyword is not provided, it redirects to the home page.
    if keyword == None:
        return redirect("/")
    # If the keyword is already in db, it fetches the stored jobs.
    if keyword in db:
        jobs = db[keyword]
    # If not, it scrapes jobs from Indeed, We Work Remotely, and RemoteOK, aggregates them, and stores them in db.
    else:
        indeed = extract_indeed_jobs (keyword)
        wwr = extract_wwr_jobs (keyword)
        remoteok = extract_remoteok_jobs(keyword)
        jobs = indeed + wwr + remoteok
        db[keyword] = jobs
    # Renders search.html and passes the keyword and jobs to the template.
    return render_template("search.html", keyword = keyword, jobs=jobs)

# Allows the user to export the job listings for a specific keyword.
@app.route("/export")
def export ():
    # Captures the keyword from the request arguments.
    keyword = request.args.get("keyword")
    # If keyword is not provided or not in db, it redirects appropriately.
    if keyword == None:
        return redirect("/")
    # If keyword is valid and in db, it calls save_to_file to create a CSV file and then sends this file to the user.
    if keyword not in db:
        return redirect (f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file (f"{keyword}.csv", as_attachment=True)

if __name__ == "__main__":
    app.run()
