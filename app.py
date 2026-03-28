import streamlit as st
import json
import io
import fitz  # PyMuPDF
import html
from docx import Document
from main import run_research_agent, DEFAULT_MODEL

# -----------------------------
# Available Gemini Models
# -----------------------------
AVAILABLE_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-1.5-pro"
]

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Advanced Therapies Test Case Generator",
    page_icon="🧪",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px;
}
.main-title {
    font-size: 2.35rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
}
.subtitle {
    color: var(--text-color);
    opacity: 0.72;
    margin-bottom: 1.2rem;
}
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0.42rem 0.9rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    font-size: 0.92rem;
    color: var(--text-color);
}
.success-chip {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.85rem;
    margin-top: 0.4rem;
    margin-bottom: 0.7rem;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(16, 185, 129, 0.12);
    color: var(--text-color);
}
.user-row {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 12px;
    margin: 18px 0 20px 0;
    width: 100%;
}
.assistant-row {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 12px;
    margin: 18px 0 12px 0;
    width: 100%;
}
.chat-avatar {
    width: 42px;
    height: 42px;
    min-width: 42px;
    min-height: 42px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    border: 1px solid rgba(255,255,255,0.08);
}
.user-avatar {
    background: linear-gradient(135deg, #ff4b4b, #ff2e63);
    color: white;
}
.assistant-avatar {
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: white;
}
.user-bubble-wrap {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    max-width: 82%;
}
.user-bubble {
    width: fit-content;
    max-width: 100%;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.98), rgba(15, 23, 42, 0.98));
    color: white;
    padding: 16px 18px;
    border-radius: 20px;
    border-top-right-radius: 7px;
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 1rem;
    line-height: 1.75;
    box-shadow: 0 10px 28px rgba(0,0,0,0.22);
    white-space: pre-wrap;
}
.user-meta {
    font-size: 0.82rem;
    opacity: 0.68;
    margin-top: 7px;
    text-align: right;
    padding-right: 4px;
}
.attachment-card {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.20);
    color: var(--text-color);
    padding: 0.9rem 1rem;
    border-radius: 14px;
    margin-top: 0.7rem;
    font-size: 0.95rem;
    max-width: 100%;
}
.assistant-wrap {
    width: min(100%, 880px);
}
.assistant-label {
    font-size: 0.9rem;
    opacity: 0.72;
    margin-bottom: 0.55rem;
    margin-left: 2px;
    font-weight: 600;
}
.section-title {
    font-size: 1.04rem;
    font-weight: 700;
    margin-top: 0.9rem;
    margin-bottom: 0.45rem;
    color: var(--text-color);
}
.result-card {
    background: rgba(255, 255, 255, 0.045);
    color: var(--text-color);
    padding: 1rem 1.1rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.10);
    line-height: 1.7;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 15px;
}
th, td {
    border: 1px solid rgba(255,255,255,0.10);
    padding: 12px;
    text-align: left;
    vertical-align: top;
}
th {
    background: rgba(255,255,255,0.08);
}
td {
    background: rgba(255,255,255,0.03);
}
[data-testid="stChatInput"] {
    position: sticky;
    bottom: 0;
    z-index: 999;
    padding-top: 0.7rem;
    background: linear-gradient(to top, rgba(14,17,23,1), rgba(14,17,23,0.92), rgba(14,17,23,0));
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

# -----------------------------
# File Extraction
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"[Error reading PDF: {e}]"

def extract_text_from_docx(uploaded_file):
    try:
        file_stream = io.BytesIO(uploaded_file.read())
        doc = Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        return f"[Error reading DOCX: {e}]"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.gemini_api_key
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Key", use_container_width=True):
            st.session_state.gemini_api_key = api_key_input.strip()
            st.success("Saved")
    with col2:
        if st.button("🗑 Clear Key", use_container_width=True):
            st.session_state.gemini_api_key = ""
            st.rerun()

    if st.session_state.gemini_api_key:
        st.markdown("<div class='success-chip'>✅ API key loaded</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No API key set")

    st.divider()

    selected_model = st.selectbox(
        "Choose Gemini Model",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(st.session_state.selected_model)
        if st.session_state.selected_model in AVAILABLE_MODELS else 0
    )
    st.session_state.selected_model = selected_model

    st.divider()

    st.markdown("### 📎 Optional Attachment")
    uploaded_file = st.file_uploader(
        "Upload supporting file (optional)",
        type=["pdf", "docx"]
    )

    attachment_description = st.text_area(
        "Attachment Description (optional)",
        placeholder="Describe what this file contains..."
    )

    st.divider()

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🧪 Advanced Therapies Test Case Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate structured manual QA test cases from requirements and optional attachments.</div>',
    unsafe_allow_html=True
)
st.markdown(
    f"<div class='model-badge'>🤖 Model: {st.session_state.selected_model}</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Render Functions
# -----------------------------
def render_user_message(text, attachment_name=None, attachment_desc=None):
    # Keep user content safe and prevent HTML injection in rendered text
    safe_text = html.escape(text)
    attachment_html = ""
    if attachment_name or attachment_desc:
        attachment_html += "<div class='attachment-card'>"
        if attachment_name:
            attachment_html += f"<b>📎 Attachment:</b> {html.escape(attachment_name)}<br>"
        if attachment_desc:
            attachment_html += f"<b>📝 Description:</b> {html.escape(attachment_desc)}"
        attachment_html += "</div>"

    st.markdown(f"""
    <div class="user-row">
        <div class="user-bubble-wrap">
            <div class="user-bubble">{safe_text}</div>
            {attachment_html}
        </div>
        <div class="chat-avatar user-avatar">👤</div>
    </div>
    """, unsafe_allow_html=True)

def render_assistant_header():
    st.markdown("""
    <div class="assistant-row">
        <div class="chat-avatar assistant-avatar">🤖</div>
        <div class="assistant-wrap">
            <div class="assistant-label">Generated Test Case</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_result(result):
    st.markdown(f"<div class='section-title'>🆔 Test Case ID</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-card'>{result.get('test_case_id','')}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-title'>📌 Summary</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-card'>{result.get('summary','')}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-title'>📋 Precondition</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='result-card'>" +
        "<br>".join([f"• {x}" for x in result.get("precondition", [])]) +
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(f"<div class='section-title'>🧭 Main Steps</div>", unsafe_allow_html=True)
    table_html = """
    <table>
        <tr>
            <th>Step</th>
            <th>Action</th>
            <th>Expected Result</th>
        </tr>
    """
    for step in result.get("main_steps", []):
        table_html += f"""
        <tr>
            <td>{step.get('step','')}</td>
            <td>{step.get('action','')}</td>
            <td>{step.get('expected_result','')}</td>
        </tr>
        """
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown(f"<div class='section-title'>✅ Postcondition</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='result-card'>" +
        "<br>".join([f"• {x}" for x in result.get("postcondition", [])]) +
        "</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='section-title'>📚 Sources</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='result-card'>" +
            "<br>".join([f"• {x}" for x in result.get("sources", [])]) +
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(f"<div class='section-title'>🛠 Tools Used</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='result-card'>" +
            "<br>".join([f"• {x}" for x in result.get("tools_used", [])]) +
            "</div>",
            unsafe_allow_html=True
        )

# -----------------------------
# Render ALL old chat messages
# -----------------------------
for msg in st.session_state.chat_messages:
    if msg["role"] == "user":
        render_user_message(
            msg["content"],
            msg.get("attachment_name"),
            msg.get("attachment_desc")
        )
    elif msg["role"] == "assistant":
        render_assistant_header()
        render_result(msg["content"])

# -----------------------------
# Chat input
# -----------------------------
query = st.chat_input("Paste your requirement here...")

if query:
    if not st.session_state.gemini_api_key:
        st.error("❌ Please enter your Gemini API key first.")
        st.stop()

    attachment_text = ""
    attachment_name = None

    if uploaded_file is not None:
        attachment_name = uploaded_file.name
        if uploaded_file.type == "application/pdf":
            attachment_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            attachment_text = extract_text_from_docx(uploaded_file)

    # Store USER message first
    st.session_state.chat_messages.append({
        "role": "user",
        "content": query,
        "attachment_name": attachment_name,
        "attachment_desc": attachment_description,
        "attachment_text": attachment_text
    })

    # Immediately rerender user message
    render_user_message(query, attachment_name, attachment_description)

    # Assistant response
    render_assistant_header()
    with st.spinner(f"Generating with {st.session_state.selected_model}..."):
        try:
            result = run_research_agent(
                messages=st.session_state.chat_messages,
                api_key=st.session_state.gemini_api_key,
                model_name=st.session_state.selected_model,
                attachment_text=attachment_text,
                attachment_description=attachment_description
            )

            result_dict = result.model_dump()

            # Store ASSISTANT response
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result_dict
            })

            render_result(result_dict)

        except Exception as e:
            st.error(f"❌ Error: {e}")