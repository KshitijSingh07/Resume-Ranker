"""
Job description parser module.
Uses recruiter-selected domain and optional JD to derive required skills.
"""

from __future__ import annotations

from typing import List

from config import DOMAIN_SKILLS


def extract_required_skills(selected_domain: str, job_description: str) -> List[str]:
    """
    Extract required skills from selected domain that appear in JD.
    If JD is empty or no skill is detected, return all selected domain skills.
    """
    domain_skills = DOMAIN_SKILLS.get(selected_domain, [])
    jd_text = (job_description or "").lower().strip()

    # If JD is not provided, use only domain skills.
    if not jd_text:
        return domain_skills

    required = [skill for skill in domain_skills if skill in jd_text]
    if required:
        return required

    # If JD does not mention known domain skills, keep full domain list.
    return domain_skills
