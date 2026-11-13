import json
import logging
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.matching.models import MatchResult
from src.parsing.validators import max_upload_bytes
from src.pipeline import analyze_resume
from src.utils.errors import SkillMatchError

ROOT = Path(__file__).resolve().parents[2]
LOGGER = logging.getLogger(__name__)
load_dotenv(ROOT / ".env")


def _render_results(result: MatchResult, label: str = "") -> None:
    st.subheader("Results")
    if label:
        st.text(f"Resume: {label}")
    st.metric("Match score", f"{result.breakdown.final_score:.0f} / 100")
    st.progress(result.breakdown.final_score / 100)

    left, middle, right = st.columns(3)
    with left:
        st.markdown("**Matched skills**")
        for hit in result.matched:
            st.write(f"✓ {hit.skill.name}")
    with middle:
        st.markdown("**Skills to add**")
        for skill in result.missing:
            st.write(f"+ {skill.name}")
    with right:
        st.markdown("**Extra skills**")
        for skill in result.extra:
            st.write(f"• {skill.name}")

    with st.expander("Why this score?"):
        breakdown = result.breakdown
        st.write(
            f"Required coverage: {breakdown.required_coverage:.0%} "
            f"(60% weight before redistribution)"
        )
        st.write(f"Preferred coverage: {breakdown.preferred_coverage:.0%} (20% weight)")
        st.write(
            f"Text similarity: {breakdown.semantic_similarity:.0%} "
            f"(20% weight; {result.method})"
        )
        st.caption(
            "Score = 60% required coverage + 20% preferred coverage + "
            "20% text similarity. When no preferred skills are listed, their "
            "weight is added to required coverage."
        )
    with st.expander("Resume evidence"):
        if not result.matched:
            st.write("No matching skills were found.")
        for hit in result.matched:
            st.markdown(f"**{hit.skill.name}**")
            for snippet in hit.evidence:
                st.text(snippet)


def _load_roles() -> dict[str, str]:
    roles: dict[str, str] = {}
    roles_path = ROOT / "data" / "roles"
    for path in sorted(roles_path.glob("*.json")):
        role = json.loads(path.read_text(encoding="utf-8"))
        roles[role["name"]] = role["description"]
    return roles


def _job_description(key: str) -> str:
    roles = _load_roles()
    mode = st.radio(
        "Job description source",
        ("Preset role", "Paste a job description"),
        key=f"{key}_jd_mode",
        horizontal=True,
    )
    if mode == "Preset role":
        name = st.selectbox("Choose a target role", sorted(roles), key=f"{key}_role")
        return roles[name]
    return st.text_area("Paste a job description", key=f"{key}_jd", height=180)


def _show_error(error: Exception) -> None:
    st.error(str(error))


def main() -> None:
    st.set_page_config(page_title="SkillMatch", page_icon="🎯", layout="wide")
    st.title("SkillMatch")
    st.caption("Know your fit before you apply.")
    st.info(
        "SkillMatch is decision support, not a hiring decision. Files are processed "
        "locally for this analysis and are not saved by the app."
    )
    st.caption(
        f"Maximum upload size: {max_upload_bytes() // (1024 * 1024)} MB per file."
    )

    single_tab, batch_tab = st.tabs(["Single resume", "Batch ranking"])
    with single_tab:
        upload = st.file_uploader(
            "Upload a text-based PDF or DOCX resume",
            type=["pdf", "docx"],
            key="single_resume",
        )
        jd = _job_description("single")
        if st.button("Analyze resume", type="primary", key="analyze_single"):
            if upload is None:
                st.error("Upload a resume to continue.")
            elif not jd.strip():
                st.error("Choose a role or enter a job description.")
            else:
                try:
                    result = analyze_resume(upload.name, upload.getvalue(), jd)
                    _render_results(result)
                except SkillMatchError as exc:
                    _show_error(exc)
                # This UI boundary hides unexpected dependency details from users.
                except Exception as exc:  # noqa: BLE001
                    LOGGER.error(
                        "Unexpected error analyzing a resume (%s).",
                        type(exc).__name__,
                    )
                    st.error("Something went wrong while analyzing this resume.")

    with batch_tab:
        uploads = st.file_uploader(
            "Upload multiple PDF or DOCX resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="batch_resumes",
        )
        batch_jd = _job_description("batch")
        if st.button("Rank resumes", type="primary", key="analyze_batch"):
            if not uploads:
                st.error("Upload at least one resume to continue.")
            elif not batch_jd.strip():
                st.error("Choose a role or enter a job description.")
            else:
                rows: list[dict[str, str | float]] = []
                results: list[tuple[str, MatchResult]] = []
                for uploaded in uploads:
                    try:
                        result = analyze_resume(
                            uploaded.name, uploaded.getvalue(), batch_jd
                        )
                        rows.append(
                            {
                                "Resume": uploaded.name,
                                "Score": result.breakdown.final_score,
                            }
                        )
                        results.append((uploaded.name, result))
                    except SkillMatchError as exc:
                        st.text(f"Resume: {uploaded.name}")
                        st.warning(str(exc))
                    except Exception as exc:  # noqa: BLE001
                        LOGGER.error(
                            "Unexpected error in batch analysis (%s).",
                            type(exc).__name__,
                        )
                        st.text(f"Resume: {uploaded.name}")
                        st.warning("Analysis failed unexpectedly.")
                if rows:
                    table = pd.DataFrame(rows).sort_values("Score", ascending=False)
                    st.dataframe(table, hide_index=True, use_container_width=True)
                    st.download_button(
                        "Download ranking CSV",
                        table.to_csv(index=False).encode("utf-8"),
                        "skillmatch_ranking.csv",
                        "text/csv",
                    )
                    with st.expander("Individual results and evidence"):
                        for name, result in results:
                            _render_results(result, name)
                else:
                    st.error("No resumes could be analyzed.")


if __name__ == "__main__":
    main()
