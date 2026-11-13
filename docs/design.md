# Design Document — SkillMatch UI/UX

Streamlit, single page, two-column layout. Simple, clean, readable on a projector.

## 1. Principles
- One screen, one flow: input -> result.
- Explain everything: no score without reasons.
- Projector-friendly: large text, high contrast, no tiny chips.

## 2. Layout (wireframe)
```
+--------------------------------------------------------------+
| SkillMatch — know your fit before you apply                  |
+----------------------+---------------------------------------+
| 1. Upload resume     |  RESULT                               |
|    [PDF / DOCX]      |  +-------------------------------+    |
|                      |  |  Match score: 72 / 100        |    |
| 2. Target role       |  |  [=========>        ]         |    |
|  ( ) Preset role     |  +-------------------------------+    |
|  ( ) Paste JD        |  Matched skills   (green chips)       |
|  [ text area ]       |  Missing skills   (red chips)         |
|                      |  Extra skills     (grey chips)        |
| [ Analyze ]          |  > Why this score? (expander)         |
+----------------------+  > Evidence from your resume          |
                       |  [Download report]                    |
                       +---------------------------------------+
| Disclaimer: decision support only. Files are not stored.     |
+--------------------------------------------------------------+
```

## 3. Components
| Component | Streamlit element | Notes |
|---|---|---|
| Uploader | `st.file_uploader(type=["pdf","docx"])` | Size limit shown beside it |
| Role input | `st.radio` + `st.selectbox` / `st.text_area` | Presets load a JD from `data/roles/` |
| Analyze | `st.button` (primary) | Disabled until both inputs exist |
| Score | `st.metric` + `st.progress` | Color band: <40 red, 40-70 amber, >70 green |
| Skill chips | `st.badge` or colored markdown | Matched = green, missing = red, extra = grey |
| Explanation | `st.expander` | Formula, weights, coverage numbers, method used |
| Evidence | `st.expander` | Snippets rendered as plain text, never HTML |
| Batch (Should) | `st.tabs(["Single","Batch"])` | Table sorted by score, CSV download |

## 4. States
| State | Behaviour |
|---|---|
| Empty | Helper text: "Upload a resume and choose a role to begin" |
| Loading | `st.spinner("Analyzing...")` |
| Success | Results as above |
| Scanned/empty PDF | "We couldn't read text from this PDF. Please upload a text-based PDF." |
| Wrong file/too large | Short specific message with the limit |
| Fallback used | Small caption: "Using TF-IDF similarity (offline fallback)" |

## 5. Copy guidelines
Plain, friendly, specific. Say "Skills to add" instead of "Deficiencies". Always show the disclaimer.

## 6. Accessibility
Don't rely on color alone: prefix chips with a symbol (check for matched, plus for missing). Min body text size per Streamlit defaults; test at projector resolution.

## 7. Visual style
Streamlit default light theme with one accent color set in `.streamlit/config.toml` (e.g. teal). No custom CSS unless time remains.
