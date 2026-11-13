import json

import pytest

from src.extraction.taxonomy import load_taxonomy
from src.utils.errors import TaxonomyError


def test_loads_canonical_skills_and_aliases(tmp_path):
    path = tmp_path / "skills.json"
    path.write_text(
        json.dumps(
            [{"name": "Machine Learning", "category": "AI/ML", "aliases": ["ML"]}]
        ),
        encoding="utf-8",
    )

    taxonomy = load_taxonomy(path)

    assert taxonomy["machine learning"] == taxonomy["ml"]
    assert taxonomy["ml"].name == "Machine Learning"


def test_rejects_conflicting_aliases(tmp_path):
    path = tmp_path / "skills.json"
    path.write_text(
        json.dumps(
            [
                {"name": "Python", "category": "Programming", "aliases": ["Py"]},
                {"name": "PyTorch", "category": "AI/ML", "aliases": ["Py"]},
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(TaxonomyError, match="Alias conflicts"):
        load_taxonomy(path)


def test_rejects_non_list_taxonomy(tmp_path):
    path = tmp_path / "skills.json"
    path.write_text("{}", encoding="utf-8")

    with pytest.raises(TaxonomyError, match="JSON list"):
        load_taxonomy(path)
