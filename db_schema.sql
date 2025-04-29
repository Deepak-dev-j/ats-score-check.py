CREATE DATABASE ats_resume;
USE ats_resume;

CREATE TABLE resume_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(100),
    score FLOAT,
    matched_keywords TEXT
);
