import streamlit as st
from openai import OpenAI

# OpenAI client will read OPENAI_API_KEY from your env
client = OpenAI()

SYSTEM_PROMPT = """
You are an SRE / DevOps copilot that explains incidents clearly.
Given raw logs, you will:
- Summarize what happened in plain English
- Highlight likely root cause(s)
- Suggest 3–5 things to check first
Keep it concise and structured for on-call engineers.
"""

st.set_page_config(
    page_title="DevOps Copilot – Incident Triage",
    page_icon="🛠️",
)

st.title("🛠️ LLM DevOps Copilot for Incident Triage")
st.write(
    "Paste incident logs or upload a log file, and the copilot will explain "
    "what’s going on, likely root cause, and what to check first."
)

# --- Input area: paste logs ---
logs_text = st.text_area("Paste logs here", height=200)

# --- Optional: upload a .txt/.log file ---
uploaded = st.file_uploader(
    "…or upload a log file (.txt / .log)", type=["txt", "log"]
)

if uploaded is not None:
    file_content = uploaded.read().decode("utf-8", errors="ignore")
    # If textarea is empty, just use the file
    if not logs_text.strip():
        logs_text = file_content
    else:
        # Append file content below pasted text
        logs_text = logs_text + "\n" + file_content

analyze_clicked = st.button("Analyze incident")

if analyze_clicked:
    if not logs_text.strip():
        st.warning("Please paste logs or upload a file first.")
    else:
        with st.spinner("Asking the copilot…"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": logs_text},
                ],
            )
            answer = response.choices[0].message.content

        st.subheader("📋 Copilot Summary")
        st.markdown(answer)
