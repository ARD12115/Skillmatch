from src.matching.models import Skill
from src.ui import app


def test_analyze_resume_uses_taxonomy_and_strips_contact_from_similarity(
    monkeypatch,
):
    observed = {}
    taxonomy = {
        "python": Skill("Python", "Programming"),
        "docker": Skill("Docker", "Cloud/DevOps"),
    }

    monkeypatch.setattr(
        app, "_read_resume", lambda *_: "Email: student@example.com\nPython developer"
    )
    monkeypatch.setattr(app, "get_taxonomy", lambda: taxonomy)

    def fake_similarity(resume, jd):
        observed.update(resume=resume, jd=jd)
        return 0.5, "tfidf"

    monkeypatch.setattr(app, "semantic_similarity", fake_similarity)

    result = app.analyze_resume(
        "resume.pdf",
        b"%PDF-fake",
        "Required:\nPython\nPreferred:\nDocker",
    )

    assert "student@example.com" not in observed["resume"]
    assert "Python developer" in observed["resume"]
    assert [hit.skill.name for hit in result.matched] == ["Python"]
    assert [skill.name for skill in result.missing] == ["Docker"]
    assert result.method == "tfidf"
