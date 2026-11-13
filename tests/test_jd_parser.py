from src.extraction.jd_parser import split_required_preferred
from src.matching.models import Skill


def taxonomy():
    python = Skill("Python", "Programming")
    sql = Skill("SQL", "Databases")
    docker = Skill("Docker", "Cloud/DevOps")
    return {"python": python, "sql": sql, "docker": docker}


def test_splits_required_and_preferred_skills():
    result = split_required_preferred(
        "Required Skills:\nPython\nSQL\nNice to have:\nDocker", taxonomy()
    )

    assert [hit.skill.name for hit in result.required] == ["Python", "SQL"]
    assert [hit.skill.name for hit in result.preferred] == ["Docker"]


def test_unheaded_description_defaults_to_required_and_empty_is_safe():
    result = split_required_preferred("Python and SQL", taxonomy())
    empty = split_required_preferred("", taxonomy())

    assert {hit.skill.name for hit in result.required} == {"Python", "SQL"}
    assert result.preferred == []
    assert empty.required == []
    assert empty.preferred == []


def test_skill_listed_in_both_sections_is_required_only():
    result = split_required_preferred(
        "Required:\nPython\nPreferred:\nPython and Docker", taxonomy()
    )

    assert [hit.skill.name for hit in result.required] == ["Python"]
    assert [hit.skill.name for hit in result.preferred] == ["Docker"]


def test_inline_heading_content_is_included():
    result = split_required_preferred(
        "Required: Python\nPreferred: Docker", taxonomy()
    )

    assert [hit.skill.name for hit in result.required] == ["Python"]
    assert [hit.skill.name for hit in result.preferred] == ["Docker"]
