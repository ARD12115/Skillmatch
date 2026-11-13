import json
from pathlib import Path
from typing import Any

from src.matching.models import Skill
from src.utils.errors import TaxonomyError


def load_taxonomy(path: str | Path) -> dict[str, Skill]:
    """Load canonical skills and aliases from a JSON taxonomy file."""
    taxonomy_path = Path(path)
    try:
        raw: Any = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaxonomyError(f"Unable to load skill taxonomy: {taxonomy_path}") from exc

    if not isinstance(raw, list):
        raise TaxonomyError("Skill taxonomy must be a JSON list.")

    taxonomy: dict[str, Skill] = {}
    seen_names: set[str] = set()
    for entry in raw:
        if not isinstance(entry, dict):
            raise TaxonomyError("Each taxonomy entry must be an object.")
        name = entry.get("name")
        category = entry.get("category")
        aliases = entry.get("aliases", [])
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(category, str)
            or not category.strip()
            or not isinstance(aliases, list)
            or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)
        ):
            raise TaxonomyError("Taxonomy entries need a name, category, and string aliases.")

        skill = Skill(name=name.strip(), category=category.strip())
        normalized_name = skill.name.casefold()
        if normalized_name in seen_names:
            raise TaxonomyError(f"Duplicate canonical skill: {skill.name}")
        seen_names.add(normalized_name)
        for term in [skill.name, *aliases]:
            key = term.strip().casefold()
            existing = taxonomy.get(key)
            if existing is not None and existing != skill:
                raise TaxonomyError(f"Alias conflicts with another skill: {term}")
            taxonomy[key] = skill
    return taxonomy
