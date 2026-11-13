from src.extraction.extractor import extract_skills
from src.matching.models import Skill


def make_taxonomy():
    python = Skill("Python", "Programming")
    machine_learning = Skill("Machine Learning", "AI/ML")
    cpp = Skill("C++", "Programming")
    return {
        "python": python,
        "machine learning": machine_learning,
        "ml": machine_learning,
        "c++": cpp,
    }


def test_extracts_canonical_alias_punctuation_and_evidence():
    hits = extract_skills(
        "Built projects with PYTHON and ML. Used C++ in coursework.", make_taxonomy()
    )

    assert [hit.skill.name for hit in hits] == [
        "Python",
        "Machine Learning",
        "C++",
    ]
    assert all(hit.evidence for hit in hits)
    assert "ML" in hits[1].evidence[0]


def test_empty_unknown_and_duplicate_mentions():
    taxonomy = make_taxonomy()

    assert extract_skills("", taxonomy) == []
    assert extract_skills("Ruby only", taxonomy) == []
    hits = extract_skills("Python, Python, and Python projects.", taxonomy)
    assert len(hits) == 1
    assert len(hits[0].evidence) <= 2


def test_fuzzy_match_handles_small_typo():
    hits = extract_skills("I have experiance with Python.", make_taxonomy())

    assert [hit.skill.name for hit in hits] == ["Python"]
