from src import pipeline
from src.matching.models import Skill


def test_analyze_resume_scores_only_skills_not_demographic_details(monkeypatch):
    observed: list[tuple[str, str]] = []
    resume_texts = iter(
        [
            "Name: Alice\nAge: 20\nCollege: North\nEmail: alice@example.com\nPython developer",
            "Name: Bob\nAge: 24\nCollege: South\nEmail: bob@example.com\nPython developer",
        ]
    )
    taxonomy = {
        "python": Skill("Python", "Programming"),
        "docker": Skill("Docker", "Cloud/DevOps"),
    }

    monkeypatch.setattr(pipeline, "_read_resume", lambda *_: next(resume_texts))
    monkeypatch.setattr(pipeline, "_load_taxonomy", lambda: taxonomy)

    def fake_similarity(resume: str, jd: str) -> tuple[float, str]:
        observed.append((resume, jd))
        return 0.5, "tfidf"

    monkeypatch.setattr(pipeline, "semantic_similarity", fake_similarity)

    first = pipeline.analyze_resume(
        "first.pdf", b"%PDF-fake", "Required:\nPython\nPreferred:\nDocker"
    )
    second = pipeline.analyze_resume(
        "second.pdf", b"%PDF-fake", "Required:\nPython\nPreferred:\nDocker"
    )

    assert observed == [("Python", "Python Docker"), ("Python", "Python Docker")]
    assert first.breakdown.final_score == second.breakdown.final_score
    assert [hit.skill.name for hit in first.matched] == ["Python"]
    assert [skill.name for skill in first.missing] == ["Docker"]
    assert first.method == "tfidf"
