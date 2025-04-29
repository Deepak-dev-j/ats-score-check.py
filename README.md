# ATS Resume Score Analyzer (GUI Version)

This project is a GUI-based Resume Analyzer that scores resumes based on keyword matching with a job description, simulating an ATS (Applicant Tracking System).

## Features

- Upload a resume (PDF)
- Input job description
- Analyze and score based on matched keywords
- Store results in MySQL database

## Technologies

- Python
- Tkinter (GUI)
- PyPDF2
- MySQL
- NLTK

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Setup the MySQL database using `db_schema.sql`.

3. Run the GUI:
   ```bash
   python ats_resume_gui.py
   ```

## Database Schema

```sql
CREATE DATABASE ats_resume;
USE ats_resume;

CREATE TABLE resume_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(100),
    score FLOAT,
    matched_keywords TEXT
);
```

## Author

Deepak J
