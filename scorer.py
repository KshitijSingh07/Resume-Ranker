"""
Scoring engine for resume ranking.
"""

from __future__ import annotations

import re
from typing import Dict, List


def compute_skill_score(resume_text: str, required_skills: List[str]) -> Dict[str, object]:
    """
    Skill scoring:
    - Only selected-domain required skills are considered.
    - Each matched skill gives +15.
    """
    matched = [skill for skill in required_skills if skill in resume_text]
    skill_score = float(len(matched) * 15)
    return {"skill_score": skill_score, "matched_skills": matched}


def compute_domain_priority_score(resume_text: str, domain_skills: List[str]) -> Dict[str, float]:
    """
    Domain priority rule:
    - If resume has at least one selected domain skill: +30 bonus.
    - If resume has no selected domain skill: -30 penalty.
    """
    has_domain_skill = any(skill in resume_text for skill in domain_skills)
    domain_bonus_or_penalty = 30.0 if has_domain_skill else -30.0
    return {"domain_bonus_or_penalty": domain_bonus_or_penalty}


def extract_experience_years(resume_text: str) -> float:
    """
    Extract max years of experience from patterns like:
    - 2 years
    - 3 yrs
    - 4 year
    """
    pattern = r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?)"
    matches = re.findall(pattern, resume_text)
    if not matches:
        return 0.0
    return max(float(value) for value in matches)


def compute_experience_score(resume_text: str) -> float:
    """
    Experience scoring:
    - Each year gives +5.
    """
    years = extract_experience_years(resume_text)
    return years * 5.0


def compute_project_score(resume_text: str) -> float:
    """
    Project scoring:
    - If any project keyword is present, +20.
    """
    project_keywords = ["github", "project", "built", "developed"]
    has_project_signal = any(keyword in resume_text for keyword in project_keywords)
    return 20.0 if has_project_signal else 0.0


def compute_education_score(resume_text: str) -> float:
    """
    Education scoring:
    - bachelor: +10
    - master: +15
    - phd: +20
    """
    if "phd" in resume_text or "doctorate" in resume_text:
        return 20.0
    if "master" in resume_text or "m.tech" in resume_text or "msc" in resume_text:
        return 15.0
    if "bachelor" in resume_text or "b.tech" in resume_text or "bsc" in resume_text:
        return 10.0
    return 0.0


def compute_final_score(
    similarity: float,
    skill_score: float,
    experience_score: float,
    project_score: float,
    education_score: float,
    domain_bonus_or_penalty: float,
) -> float:
    """
    Final weighted score:
    (similarity * 30) + skill + experience + project + education + domain_bonus_or_penalty
    """
    return (
        (similarity * 30.0)
        + skill_score
        + experience_score
        + project_score
        + education_score
        + domain_bonus_or_penalty
    )
