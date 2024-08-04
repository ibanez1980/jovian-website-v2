from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)

    if not job:
        return "Not Found", 404

    return render_template("jobpage.html", job=job)

@app.route("/job/<id>/apply", methods=["POST"])
def apply_to_job(id):
    data = request.form.to_dict()
    logger.info(f"Received application data: {data}")

    job = load_job_from_db(id)
    if not job:
        return "Job not found", 404

    try:
        add_application_to_db(id, data)
        logger.info("Application added to the database")
    except Exception as e:
        logger.error(f"Error adding application to database: {e}")
        return "An error occurred while processing your application", 500

    return render_template("application_submitted.html", application=data, job=job)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)