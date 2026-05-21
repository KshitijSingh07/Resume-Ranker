"""
Entry point for modular Resume Ranking System.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from config import DOMAIN_SKILLS
from jd_parser import extract_required_skills
from parser import extract_text_from_pdf
from scorer import (
    compute_domain_priority_score,
    compute_education_score,
    compute_experience_score,
    compute_final_score,
    compute_project_score,
    compute_skill_score,
)
from utils import compute_tfidf_similarity


def load_resumes(resume_folder: Path) -> Dict[str, str]:
    """
    Load all PDF resumes from folder and return {filename: extracted_text}.
    """
    resume_texts: Dict[str, str] = {}

    if not resume_folder.exists():
        print(f"Resume folder not found: {resume_folder}")
        return resume_texts

    pdf_files = sorted(resume_folder.glob("*.pdf"))
    for pdf_file in pdf_files:
        try:
            text = extract_text_from_pdf(str(pdf_file))
            resume_texts[pdf_file.name] = text
        except Exception as exc:  # noqa: BLE001
            print(f"Skipping {pdf_file.name}: {exc}")

    return resume_texts


def get_domain_from_user() -> str:
    """
    Ask recruiter to select a domain and return domain key.
    """
    domain_options = {
        "1": ("Web Dev", "web_dev"),
        "2": ("Data Science", "data_science"),
        "3": ("AI/ML", "ai_ml"),
        "4": ("Cybersecurity", "cyber_security"),
        "5": ("Cloud/DevOps", "cloud_devops"),
        "6": ("Mobile Dev", "mobile_dev"),
        "7": ("SDE", "sde"),
        "8": ("UI/UX", "ui_ux"),
        "9": ("Blockchain", "blockchain"),
    }

    print("Select domain:")
    print("(1) Web Dev")
    print("(2) Data Science")
    print("(3) AI/ML")
    print("(4) Cybersecurity")
    print("(5) Cloud/DevOps")
    print("(6) Mobile Dev")
    print("(7) SDE")
    print("(8) UI/UX")
    print("(9) Blockchain")

    while True:
        choice = input("Enter choice (1-9): ").strip()
        if choice in domain_options:
            return domain_options[choice][1]
        print("Invalid input. Please select a number from 1 to 9.")


def get_job_description_from_user() -> str:
    """
    Ask recruiter for optional job description.
    """
    print("\nEnter job description (optional).")
    print("Press Enter directly to skip.")
    return input("Job Description: ").strip()


def rank_resumes(
    selected_domain: str, job_description: str, resume_texts: Dict[str, str]
) -> List[Dict[str, float]]:
    """
    Rank resumes with detailed score breakdown.
    Selected domain is always the top-priority signal.
    """
    domain_skills = DOMAIN_SKILLS.get(selected_domain, [])
    required_skills = extract_required_skills(selected_domain, job_description)

    filenames = list(resume_texts.keys())
    texts = [resume_texts[name] for name in filenames]

    # If JD is not provided, similarity is 0 for all resumes.
    if job_description.strip():
        similarities = compute_tfidf_similarity(job_description, texts)
    else:
        similarities = [0.0 for _ in texts]

    results = []
    for filename, resume_text, similarity in zip(filenames, texts, similarities):
        skill_data = compute_skill_score(resume_text, required_skills)
        skill_score = float(skill_data["skill_score"])
        domain_priority_data = compute_domain_priority_score(resume_text, domain_skills)
        domain_bonus_or_penalty = float(domain_priority_data["domain_bonus_or_penalty"])
        experience_score = compute_experience_score(resume_text)
        project_score = compute_project_score(resume_text)
        education_score = compute_education_score(resume_text)

        final_score = compute_final_score(
            similarity=similarity,
            skill_score=skill_score,
            experience_score=experience_score,
            project_score=project_score,
            education_score=education_score,
            domain_bonus_or_penalty=domain_bonus_or_penalty,
        )

        results.append(
            {
                "file_name": filename,
                "domain": selected_domain,
                "required_skills": required_skills,
                "similarity": similarity,
                "skill_score": skill_score,
                "experience_score": experience_score,
                "project_score": project_score,
                "education_score": education_score,
                "domain_bonus_or_penalty": domain_bonus_or_penalty,
                "final_score": final_score,
            }
        )

    results.sort(key=lambda item: item["final_score"], reverse=True)
    return results


def print_ranked_results(results: List[Dict[str, float]]) -> None:
    """
    Print ranked output in a clear ATS-like format.
    """
    if not results:
        print("No resumes found or all resumes failed to parse.")
        return

    print("\nSelected Domain:", results[0]["domain"])
    print("Required Skills:", ", ".join(results[0]["required_skills"]))
    print("-" * 70)

    for idx, item in enumerate(results, start=1):
        print(f"Rank: {idx}")
        print(f"File name: {item['file_name']}")
        print(f"Final score: {item['final_score']:.2f}")
        print(f"Skill score: {item['skill_score']:.2f}")
        print(f"Experience score: {item['experience_score']:.2f}")
        print(f"Project score: {item['project_score']:.2f}")
        print(f"Education score: {item['education_score']:.2f}")
        print(f"Similarity: {item['similarity']:.4f}")
        print(f"Domain bonus/penalty: {item['domain_bonus_or_penalty']:.2f}")
        print("-" * 70)


def main() -> None:
    """
    Main execution:
    1. Ask domain
    2. Ask optional JD
    2. Load resumes
    3. Rank
    4. Print
    """
    selected_domain = get_domain_from_user()
    job_description = get_job_description_from_user()

    resume_folder = Path(__file__).parent / "resumes"
    resume_texts = load_resumes(resume_folder)
    ranked_results = rank_resumes(selected_domain, job_description, resume_texts)
    print_ranked_results(ranked_results)


if __name__ == "__main__":
    main()
