from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)

# Log the database connection string (without sensitive details)
logger.info(f"Connecting to database with connection string: {db_connection_string}")

Session = sessionmaker(bind=engine)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = []
        for row in result.all():
            jobs.append(row._asdict())
        return jobs 

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :id"), {'id': id})
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._asdict()

def add_application_to_db(job_id, data):
    session = Session()
    try:
        query = text("""
            INSERT INTO applications 
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)
        logger.info(f"Inserting application for job_id: {job_id} with data: {data}")
        session.execute(query, {
            'job_id': job_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'linkedin_url': data['linkedin_url'],
            'education': data['education'],
            'work_experience': data['work_experience'],
            'resume_url': data['resume_url']
        })
        session.commit()
        logger.info("Application inserted successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting application: {e}")
        raise
    finally:
        session.close()
