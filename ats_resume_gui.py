import tkinter as tk
from tkinter import filedialog, messagebox
import mysql.connector
import PyPDF2
import os
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Change this
    database="ats_resume"
)
cursor = db.cursor()

# Resume Text Extractor
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text.lower()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read resume: {str(e)}")
        return ""

# Score Calculator
def calculate_score(resume_text, job_description):
    stop_words = set(stopwords.words('english'))
    job_keywords = [word.lower() for word in job_description.split() if word.lower() not in stop_words]
    matched = [word for word in job_keywords if word in resume_text]
    score = len(matched) / len(job_keywords) * 100 if job_keywords else 0
    return round(score, 2), ', '.join(set(matched))

# Save Result
def save_to_db(candidate_name, score, keywords):
    query = "INSERT INTO resume_scores (candidate_name, score, matched_keywords) VALUES (%s, %s, %s)"
    cursor.execute(query, (candidate_name, score, keywords))
    db.commit()

# GUI Logic
def upload_resume():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        resume_path.set(file_path)

def analyze_resume():
    name = name_entry.get()
    jd = job_desc_text.get("1.0", tk.END).strip()
    file_path = resume_path.get()

    if not name or not jd or not file_path:
        messagebox.showwarning("Missing Data", "Please fill all fields and upload a resume.")
        return

    resume_text = extract_text_from_pdf(file_path)
    if resume_text:
        score, matched = calculate_score(resume_text, jd)
        result_label.config(text=f"Score: {score}%\nMatched Keywords: {matched}")
        save_to_db(name, score, matched)
        messagebox.showinfo("Success", "Analysis complete and saved to database.")

# GUI Setup
root = tk.Tk()
root.title("ATS Resume Score Analyzer")
root.geometry("600x500")

tk.Label(root, text="Candidate Name:").pack()
name_entry = tk.Entry(root, width=50)
name_entry.pack()

tk.Label(root, text="Job Description:").pack()
job_desc_text = tk.Text(root, height=6, width=60)
job_desc_text.pack()

tk.Label(root, text="Upload Resume (PDF):").pack()
resume_path = tk.StringVar()
tk.Entry(root, textvariable=resume_path, width=50).pack()
tk.Button(root, text="Browse", command=upload_resume).pack()

tk.Button(root, text="Analyze", bg="green", fg="white", command=analyze_resume).pack(pady=10)

result_label = tk.Label(root, text="", fg="blue")
result_label.pack(pady=10)

root.mainloop()
