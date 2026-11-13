#!/usr/bin/env python
"""
Evaluation script for SkillMatch.
Runs the pipeline on synthetic resumes against preset JDs and computes metrics.
"""

import json
from pathlib import Path

from src.extraction.taxonomy import load_taxonomy
from src.pipeline import analyze_resume

ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "data" / "samples"
ROLES_DIR = ROOT / "data" / "roles"

# Ground truth skills for each synthetic resume (canonical names from taxonomy)
GROUND_TRUTH = {
    "resume_01_python_dev.txt": [
        "Python",
        "JavaScript",
        "SQL",
        "C++",
        "Django",
        "Flask",
        "React",
        "FastAPI",
        "PostgreSQL",
        "MongoDB",
        "Redis",
        "Git",
        "Docker",
        "AWS",
        "Linux",
        "CI/CD",
        "scikit-learn",
        "pandas",
        "NumPy",
    ],
    "resume_02_data_analyst.txt": [
        "Python",
        "R",
        "SQL",
        "pandas",
        "NumPy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "TensorFlow",
        "PyTorch",
        "XGBoost",
        "Tableau",
        "Power BI",
        "Plotly",
        "Spark",
        "Hadoop",
        "Kafka",
    ],
    "resume_03_web_dev.txt": [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Vue.js",
        "Next.js",
        "Tailwind CSS",
        "Sass",
        "Bootstrap",
        "Redux",
        "Zustand",
        "React Query",
        "Jest",
        "Cypress",
        "Node.js",
        "Express",
        "NestJS",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Docker",
        "GitHub Actions",
        "Vercel",
        "AWS",
    ],
    "resume_04_fullstack.txt": [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "Spring Boot",
        "Django",
        "Express.js",
        "MySQL",
        "PostgreSQL",
        "Redis",
        "AWS",
        "GCP",
        "Docker",
        "Kubernetes",
        "Jenkins",
        "Terraform",
        "JUnit",
        "pytest",
        "Postman",
    ],
    "resume_05_weak.txt": ["Python", "C", "HTML", "CSS", "MySQL", "Git"],
    "resume_06_devops.txt": [
        "AWS",
        "Docker",
        "Kubernetes",
        "Terraform",
        "CloudFormation",
        "Pulumi",
        "GitHub Actions",
        "GitLab CI",
        "Jenkins",
        "ArgoCD",
        "Prometheus",
        "Grafana",
        "CloudWatch",
        "Datadog",
        "Python",
        "Bash",
        "Go",
        "Linux",
        "Helm",
        "ECS",
        "Lambda",
        "RDS",
        "S3",
        "Istio",
    ],
    "resume_07_mobile.txt": [
        "Flutter",
        "Dart",
        "React Native",
        "Swift",
        "Kotlin",
        "Provider",
        "Riverpod",
        "Bloc",
        "Redux Toolkit",
        "Firebase",
        "Node.js",
        "GraphQL",
        "Fastlane",
        "GitHub Actions",
        "Codemagic",
        "Figma",
    ],
    "resume_08_qa.txt": [
        "Selenium",
        "Cypress",
        "Playwright",
        "pytest",
        "JUnit",
        "TestNG",
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "Postman",
        "RestAssured",
        "Pact",
        "JMeter",
        "k6",
        "Locust",
        "Jenkins",
        "GitHub Actions",
        "GitLab CI",
        "Appium",
        "Espresso",
        "XCUITest",
        "Jira",
        "TestRail",
        "Allure",
    ],
}


def load_jd(role_name: str) -> str:
    """Load a preset JD by role name."""
    for path in ROLES_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["name"] == role_name:
            return data["description"]
    raise ValueError(f"Role not found: {role_name}")


def evaluate():
    load_taxonomy(ROOT / "data" / "skills.json")  # ensure taxonomy loads

    # Load preset JDs
    python_jd = load_jd("Python Developer")
    data_jd = load_jd("Data Analyst")
    web_jd = load_jd("Web Developer")

    jds = {
        "Python Developer": python_jd,
        "Data Analyst": data_jd,
        "Web Developer": web_jd,
    }

    resume_files = sorted(SAMPLES_DIR.glob("resume_*.txt"))
    print(f"Found {len(resume_files)} resume files\n")

    # Results storage
    all_results = []

    for resume_path in resume_files:
        resume_name = resume_path.name
        resume_text = resume_path.read_text(encoding="utf-8")

        print(f"=== {resume_name} ===")

        # Ground truth for this resume
        gt_skills = set(GROUND_TRUTH.get(resume_name, []))
        gt_lower = {s.lower() for s in gt_skills}

        for jd_name, jd_text in jds.items():
            try:
                result = analyze_resume(resume_name, resume_text.encode(), jd_text)

                # Extract predicted skills
                matched_names = {hit.skill.name for hit in result.matched}
                missing_names = {skill.name for skill in result.missing}
                extra_names = {skill.name for skill in result.extra}
                all_predicted = matched_names | missing_names | extra_names

                # Compute precision/recall against ground truth
                predicted_lower = {s.lower() for s in all_predicted}
                tp = len(predicted_lower & gt_lower)
                fp = len(predicted_lower - gt_lower)
                fn = len(gt_lower - predicted_lower)

                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                f1 = (
                    2 * precision * recall / (precision + recall)
                    if (precision + recall) > 0
                    else 0.0
                )

                print(
                    f"  {jd_name}: Score={result.breakdown.final_score:.0f}, "
                    f"P={precision:.2f}, R={recall:.2f}, F1={f1:.2f}"
                )

                all_results.append(
                    {
                        "resume": resume_name,
                        "jd": jd_name,
                        "score": result.breakdown.final_score,
                        "precision": precision,
                        "recall": recall,
                        "f1": f1,
                        "matched": list(matched_names),
                        "missing": list(missing_names),
                        "extra": list(extra_names),
                    }
                )
            except Exception as e:  # noqa: BLE001 - broad catch for evaluation script robustness
                print(f"  {jd_name}: ERROR - {e}")

        print()

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY: Average Precision/Recall/F1 per JD")
    print("=" * 80)

    for jd_name in jds:
        jd_results = [r for r in all_results if r["jd"] == jd_name]
        if jd_results:
            avg_p = sum(r["precision"] for r in jd_results) / len(jd_results)
            avg_r = sum(r["recall"] for r in jd_results) / len(jd_results)
            avg_f1 = sum(r["f1"] for r in jd_results) / len(jd_results)
            avg_score = sum(r["score"] for r in jd_results) / len(jd_results)
            print(
                f"  {jd_name:20s}  Precision: {avg_p:.2f}  Recall: {avg_r:.2f}  F1: {avg_f1:.2f}  Avg Score: {avg_score:.0f}"
            )

    # Overall
    if all_results:
        avg_p = sum(r["precision"] for r in all_results) / len(all_results)
        avg_r = sum(r["recall"] for r in all_results) / len(all_results)
        avg_f1 = sum(r["f1"] for r in all_results) / len(all_results)
        print(
            f"\n  {'OVERALL':20s}  Precision: {avg_p:.2f}  Recall: {avg_r:.2f}  F1: {avg_f1:.2f}"
        )

    # Save detailed results
    output_path = ROOT / "data" / "evaluation_results.json"
    output_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nDetailed results saved to {output_path}")


if __name__ == "__main__":
    evaluate()
