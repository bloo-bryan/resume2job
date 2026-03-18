import os

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")


def api_get(endpoint: str) -> dict | None:
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return None


def api_post_json(endpoint: str, data: dict) -> dict | None:
    try:
        resp = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return None


def api_post_file(endpoint: str, file_bytes: bytes, filename: str, doc_type: str) -> dict | None:
    try:
        resp = requests.post(
            f"{API_BASE_URL}{endpoint}",
            files={"file": (filename, file_bytes)},
            data={"doc_type": doc_type},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return None


def api_post_text(endpoint: str, text: str, doc_type: str) -> dict | None:
    try:
        resp = requests.post(
            f"{API_BASE_URL}{endpoint}",
            data={"text": text, "doc_type": doc_type},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return None


def get_resume_text(uploaded_file: object | None, pasted_text: str) -> str | None:
    if uploaded_file:
        file_bytes = uploaded_file.read()
        with st.spinner("Parsing uploaded file..."):
            result = api_post_file("/api/parse", file_bytes, uploaded_file.name, "resume")
        if result:
            return result["raw_text"]
        return None
    if pasted_text.strip():
        return pasted_text.strip()
    return None


def render_breakdown(breakdown: dict) -> None:
    req_skills = breakdown.get("required_skills", {})
    st.markdown("**Required Skills**")
    st.progress(req_skills.get("score", 0))
    cols = st.columns(2)
    with cols[0]:
        matched = req_skills.get("matched", [])
        if matched:
            st.markdown("Matched: " + ", ".join(f":green[{s}]" for s in matched))
    with cols[1]:
        missing = req_skills.get("missing", [])
        if missing:
            st.markdown("Missing: " + ", ".join(f":red[{s}]" for s in missing))

    pref_skills = breakdown.get("preferred_skills", {})
    st.markdown("**Preferred Skills**")
    st.progress(pref_skills.get("score", 0))
    cols = st.columns(2)
    with cols[0]:
        matched = pref_skills.get("matched", [])
        if matched:
            st.markdown("Matched: " + ", ".join(f":green[{s}]" for s in matched))
    with cols[1]:
        missing = pref_skills.get("missing", [])
        if missing:
            st.markdown("Missing: " + ", ".join(f":red[{s}]" for s in missing))

    st.markdown("**Semantic Similarity**")
    st.progress(breakdown.get("semantic_similarity", 0))

    exp = breakdown.get("experience", {})
    st.markdown("**Experience**")
    st.progress(exp.get("score", 0))
    req = exp.get("required")
    det = exp.get("detected", 0)
    st.caption(f"Required: {req if req is not None else 'N/A'} yrs | Detected: {det} yrs")

    edu = breakdown.get("education", {})
    st.markdown("**Education**")
    st.progress(edu.get("score", 0))
    st.caption(
        f"Required: {edu.get('required') or 'N/A'} | Detected: {edu.get('detected') or 'N/A'}"
    )


# --- Page Config ---

st.set_page_config(page_title="Resume2Job", page_icon="\U0001f4c4", layout="wide")
st.title("Resume2Job")
st.caption("Multi-signal resume-to-job matching engine")

# --- Sidebar ---

with st.sidebar:
    st.markdown(f"**API:** `{API_BASE_URL}`")
    health = api_get("/api/health")
    if health and health.get("status") == "healthy":
        st.success("API: Connected")
    else:
        st.error("API: Unreachable")
    if health:
        st.caption(f"Models loaded: {health.get('models_loaded')}")
        st.caption(f"Qdrant connected: {health.get('qdrant_connected')}")

# --- Tabs ---

tab_match, tab_compare, tab_entities, tab_eval, tab_about = st.tabs(
    ["Match", "Comparison", "Entities", "Evaluation", "About"]
)

# --- Tab 1: Match ---

with tab_match:
    col_left, col_right = st.columns(2)
    with col_left:
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="match_file")
        resume_text = st.text_area("Or paste resume text", height=200, key="match_resume")
    with col_right:
        jd_text = st.text_area("Paste Job Description", height=300, key="match_jd")

    algorithm = st.selectbox("Algorithm", ["hybrid", "tfidf", "embedding"])

    if st.button("Analyze Match", type="primary"):
        resume = get_resume_text(resume_file, resume_text)
        jd = jd_text.strip()
        if not resume:
            st.warning("Please provide a resume (upload or paste).")
        elif not jd:
            st.warning("Please provide a job description.")
        else:
            with st.spinner("Matching..."):
                result = api_post_json(
                    "/api/match",
                    {"resume_text": resume, "jd_text": jd, "algorithm": algorithm},
                )
            if result:
                st.session_state["match_result"] = result

    if "match_result" in st.session_state:
        result = st.session_state["match_result"]
        score = result["overall_score"]
        st.metric("Overall Match Score", f"{score:.0%}")
        st.progress(score)
        st.info(result["summary"])
        with st.expander("Score Breakdown", expanded=True):
            render_breakdown(result["breakdown"])

# --- Tab 2: Comparison ---

with tab_compare:
    col_left, col_right = st.columns(2)
    with col_left:
        cmp_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="cmp_file")
        cmp_resume_text = st.text_area("Or paste resume text", height=200, key="cmp_resume")
    with col_right:
        cmp_jd_text = st.text_area("Paste Job Description", height=300, key="cmp_jd")

    if st.button("Compare All Algorithms", type="primary"):
        resume = get_resume_text(cmp_file, cmp_resume_text)
        jd = cmp_jd_text.strip()
        if not resume:
            st.warning("Please provide a resume (upload or paste).")
        elif not jd:
            st.warning("Please provide a job description.")
        else:
            with st.spinner("Comparing algorithms..."):
                result = api_post_json(
                    "/api/match/compare",
                    {"resume_text": resume, "jd_text": jd},
                )
            if result:
                st.session_state["compare_result"] = result

    if "compare_result" in st.session_state:
        result = st.session_state["compare_result"]
        cols = st.columns(3)
        for col, algo in zip(cols, ["tfidf", "embedding", "hybrid"], strict=True):
            algo_result = result[algo]
            with col:
                st.subheader(algo.upper())
                score = algo_result["overall_score"]
                st.metric("Score", f"{score:.0%}")
                st.progress(score)
                with st.expander("Breakdown"):
                    render_breakdown(algo_result["breakdown"])

        scores = {algo: result[algo]["overall_score"] for algo in ["tfidf", "embedding", "hybrid"]}
        max_delta = max(scores.values()) - min(scores.values())
        if max_delta > 0.1:
            st.warning(
                f"Algorithms disagree significantly (max delta: {max_delta:.0%}). "
                "Review the breakdowns to understand why."
            )

# --- Tab 3: Entities ---

with tab_entities:
    col_left, col_right = st.columns(2)
    with col_left:
        ent_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="ent_file")
        ent_resume_text = st.text_area("Or paste resume text", height=200, key="ent_resume")
    with col_right:
        ent_jd_text = st.text_area("Paste Job Description", height=200, key="ent_jd")

    if st.button("Extract Entities", type="primary"):
        resume = get_resume_text(ent_file, ent_resume_text)
        jd = ent_jd_text.strip()
        results = {}
        if resume:
            with st.spinner("Extracting resume entities..."):
                results["resume"] = api_post_text("/api/parse", resume, "resume")
        if jd:
            with st.spinner("Extracting JD entities..."):
                results["jd"] = api_post_text("/api/parse", jd, "job_description")
        if results:
            st.session_state["entity_results"] = results

    if "entity_results" in st.session_state:
        results = st.session_state["entity_results"]
        cols = st.columns(2)
        if "resume" in results and results["resume"]:
            with cols[0]:
                st.subheader("Resume Entities")
                entities = results["resume"]["entities"]
                st.markdown("**Skills**")
                skills = entities.get("skills", [])
                if skills:
                    st.write(", ".join(skills))
                else:
                    st.caption("No skills detected")

                exp = entities.get("experience", {})
                st.markdown(f"**Experience:** {exp.get('total_years', 0)} years")
                for pos in exp.get("positions", []):
                    title = pos.get("title", "Unknown")
                    company = pos.get("company", "")
                    st.caption(f"- {title}" + (f" at {company}" if company else ""))

                st.markdown("**Education**")
                for edu in entities.get("education", []):
                    parts = [edu.get("degree", "")]
                    if edu.get("field"):
                        parts.append(edu["field"])
                    if edu.get("institution"):
                        parts.append(edu["institution"])
                    st.caption("- " + ", ".join(parts))

        if "jd" in results and results["jd"]:
            with cols[1]:
                st.subheader("Job Description Entities")
                entities = results["jd"]["entities"]
                st.markdown("**Required Skills**")
                req = entities.get("required_skills", [])
                st.write(", ".join(req) if req else "None detected")

                st.markdown("**Preferred Skills**")
                pref = entities.get("preferred_skills", [])
                st.write(", ".join(pref) if pref else "None detected")

                min_exp = entities.get("min_experience_years")
                exp_display = min_exp if min_exp is not None else "N/A"
                st.markdown(f"**Min Experience:** {exp_display} years")

                req_edu = entities.get("required_education")
                st.markdown(f"**Required Education:** {req_edu or 'N/A'}")

# --- Tab 4: Evaluation ---

with tab_eval:
    st.info("Runs the full evaluation benchmark. This may take a minute.")
    if st.button("Run Evaluation", type="primary"):
        with st.spinner("Running evaluation benchmark..."):
            result = api_get("/api/evaluation")
        if result:
            st.session_state["eval_result"] = result

    if "eval_result" in st.session_state:
        result = st.session_state["eval_result"]
        st.metric("Test Set Size", result["test_set_size"])

        metrics = result["metrics"]
        rows = []
        for algo, m in metrics.items():
            rows.append(
                {
                    "Algorithm": algo.upper(),
                    "NDCG@5": round(m["ndcg_at_5"], 3),
                    "MRR": round(m["mrr"], 3),
                    "P@3": round(m["precision_at_3"], 3),
                }
            )
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        chart_df = df.set_index("Algorithm")
        st.bar_chart(chart_df)

        hybrid = metrics.get("hybrid", {})
        tfidf = metrics.get("tfidf", {})
        if hybrid.get("ndcg_at_5", 0) > tfidf.get("ndcg_at_5", 0):
            st.success("Hybrid outperforms TF-IDF baseline on NDCG@5.")

# --- Tab 5: About ---

with tab_about:
    st.markdown(
        """
### About Resume2Job

Resume2Job is a multi-signal resume-to-job matching engine that demonstrates
production-grade NLP engineering.

**Architecture:**
- **Parse** — PDF/DOCX ingestion and text cleaning
- **Extract** — NER-based skill, experience, and education extraction using ESCO taxonomy
- **Score** — Three-scorer architecture: TF-IDF (baseline), Embeddings (semantic),
  Structured (hard constraints)
- **Rank** — Weighted composite scoring with explainable breakdowns

**Tech Stack:**
Python, FastAPI, spaCy, sentence-transformers, scikit-learn, Qdrant, Streamlit, Docker

**Key Design Decisions:**
1. Three-scorer architecture for multi-signal matching
2. ESCO skill taxonomy (~13k skills) for robust entity recognition
3. Evaluation-first design with NDCG@5 and MRR metrics
4. Template-generated explanations (no LLM dependency)
"""
    )
