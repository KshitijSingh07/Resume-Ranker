# TF-IDF Cosine Similarity Based Resume Ranker

An AI-powered Applicant Tracking System (ATS) style Resume Ranker built using Python, TF-IDF Vectorization, and Cosine Similarity. The system automatically ranks candidate resumes against job descriptions and domain-specific skill requirements with explainable scoring.

---

## Features

- PDF Resume Parsing using `pdfplumber`
- TF-IDF + Cosine Similarity based resume matching
- Domain-specific skill evaluation
- Experience score extraction using Regex
- Education score analysis
- Project detection and scoring
- Explainable multi-component ranking system
- Supports multiple technical domains:
  - AI/ML
  - Web Development
  - Cybersecurity
  - Data Science
  - Cloud/DevOps
  - Mobile Development
  - SDE
  - UI/UX
  - Blockchain

---

## Tech Stack

- Python 3
- scikit-learn
- pdfplumber
- Regex
- TF-IDF Vectorizer
- Cosine Similarity

---

## Project Structure

```bash
resume_ranker/
│── main.py
│── config.py
│── parser.py
│── jd_parser.py
│── scorer.py
│── utils.py
│── resumes/
│── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/KshitijSingh07/Resume-Ranker.git
cd Resume-Ranker
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Add PDF resumes inside the `resumes/` folder.

Run the project:

```bash
python main.py
```

Select a domain and optionally provide a job description to rank resumes.

---

## Scoring Formula

```text
Final Score =
(TF-IDF Similarity × 30)
+ Skill Score
+ Experience Score
+ Project Score
+ Education Score
+ Domain Bonus/Penalty
```

---

## Example Features

- Detects domain-relevant skills
- Gives bonus for matching domain expertise
- Penalizes irrelevant resumes
- Provides transparent score breakdown
- Modular and scalable architecture

---

## Future Improvements

- Web-based dashboard
- OCR support for scanned PDFs
- LLM-based semantic matching
- Multi-language resume support
- Real-time job portal integration

---

## Author

**Kshitij Singh**  
B.Tech CSE, IIIT Manipur

GitHub: https://github.com/KshitijSingh07
