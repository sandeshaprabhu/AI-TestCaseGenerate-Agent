# 🧪 Advanced Therapies Test Case Generator

An AI-powered **manual QA test case generation tool** built with **LangChain + Gemini + Streamlit**.

This application is designed for **Advanced Therapies / interventional healthcare workflow requirements**, where a user can provide:

- a **requirement / user story / functional statement**
- an optional **supporting attachment** (`.pdf` / `.docx`)
- an optional **attachment description**

…and the AI will generate **structured manual test cases** in a consistent QA format.

---

## 🚀 Features

- Generate structured manual test cases
- Uses Gemini models via LangChain
- Streamlit-based chat-style UI
- Supports conversation history / chat memory
- Optional PDF/DOCX attachment upload
- Attachment description support
- API key input in UI (no need to store in .env)
- Model selection dropdown
- Dark mode friendly UI
- Clear chat support

---

## 📌 Output Format

The AI generates test cases in the following format:

- **Test Case ID**
- **Summary**
- **Precondition**
- **Main Steps**
  - Step
  - Action
  - Expected Result
- **Postcondition**
- **Sources**
- **Tools Used**

Example:

```text
Test Case ID: LOGIN-001
Summary: Verify successful user login with valid credentials

Precondition:
- Application is launched and login page is displayed
- Valid test credentials are available
- User is not already logged in

Main Steps:
1. Navigate to login page → Login page loads
2. Enter valid username → Username accepted
3. Enter valid password → Password masked correctly
4. Click Login → User redirected to dashboard
5. Verify session → Welcome message shown

Postcondition:
- User logs out and closes the application

```

## 🏗️ Tech Stack

- Python
- LangChain
- Google Gemini
- Streamlit
- Pydantic
- PyMuPDF (PDF text extraction)
- python-docx (DOCX text extraction)

## 📂 Project Structure

```text
ai-testcase-generator/
│
├── app.py              # Streamlit UI
├── main.py             # Core agent logic
├── tools.py            # Optional tools (search, wiki, save, etc.)
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignore files/folders for git
└── .env                # Optional local env file (not required)
```

## ⚙️ How It Works

1. User enters requirement
   - User prompt should describe a functional requirement, user story, or expected behavior.

2. Optional attachment upload
   - Supported: `.pdf`, `.docx`
   - Attachments may include workflow details, design specs, process notes, or test scenarios.

3. Optional attachment description
   - Provide a short summary of file content (e.g., "This document contains logout session timeout behavior").

4. AI processes input
   - App sends these to Gemini via LangChain:
     - requirement text
     - chat history context
     - extracted attachment text (if provided)
     - attachment description (if provided)

5. AI generates structured test case output
   - Output follows QA format with Test Case ID, Summary, Precondition, Main Steps, Postcondition, etc.

## 🧠 AI Agent Purpose

This tool is tailored for Advanced Therapies domain-style requirement analysis, especially for workflows involving:

- interventional procedures
- minimally invasive systems
- image-guided treatment systems
- therapy workflows
- regulated / process-heavy systems
- application behavior validation

The agent is instructed to behave like a QA / domain-aware test design assistant, not a general chatbot.

## 📦 Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/ai-testcase-generator.git
   cd ai-testcase-generator
   ```
2. Create virtual environment
   - Windows (PowerShell)
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```
   - Windows (CMD)
     ```bash
     venv\Scripts\activate.bat
     ```
   - macOS / Linux
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Run the Streamlit App

Run the command in terminal

```bash
streamlit run app.py
```

Once started, Streamlit will show a local URL like:

http://localhost:8501

Open that in your browser.

## 🔑 API Key Setup

This project does not require storing API keys in .env.

Instead:

Open the app
Go to the Settings panel in the sidebar
Paste your Gemini API Key
Click Save Key
Get Gemini API Key

You can generate your key from:

- Google AI Studio
- Gemini Developer Console

## 🧪 Supported Models

Recommended working models:

- `gemini-2.5-flash-lite`
- `gemini-2.5-flash`

⚠️ Some older / unavailable models may fail depending on your SDK/API version.

## 📝 Example Usage

### Example Requirement

The system shall allow a clinician to log out manually using the user profile menu. The application shall also automatically log out the user after 15 minutes of inactivity and redirect to the login page.

### Example Attachment Description

This file contains session timeout workflow and logout behavior.

### Example Generated Test Case

**Test Case ID:** LOGOUT-001

**Summary:** Verify user can successfully log out manually and via inactivity timeout

**Precondition:**

- Application is launched
- User is logged in
- User session is active

**Main Steps:**

1. Navigate to profile menu → Profile menu is displayed
2. Click logout option → User is logged out
3. Verify redirection → Login page is shown
4. Log in again → Session is active
5. Stay inactive for 15 minutes → Session expires automatically
6. Verify redirection → User is redirected to login page

**Postcondition:**

- User is logged out
- Application session is terminated

## 📎 Attachment Support

Supported file types:

- `.pdf`
- `.docx`

Attachment behavior:

- Optional attachment per requirement prompt
- Attachment text is used for the current invocation only
- After sending the prompt, attachment context is reset until next upload

## 🧾 Valid Attachment Use Cases

- Requirement specification document
- Functional design document
- UI flow documentation
- Workflow notes
- Validation document

## 💬 Chat Memory

The application retains conversation history during the current Streamlit session:

- previous prompts remain visible
- generated test cases remain visible
- model receives conversation context from history

Use the **Clear Chat** button in the sidebar to reset the session.

## 🎨 UI Highlights

- Chat-style layout
- User message on the right
- AI response on the left
- Dark mode-friendly design
- Attachment cards appear with prompt content
- Model badge shows selected Gemini model at top

## 🛠️ Main Files Explained

- `app.py` — Streamlit UI, sidebar settings, chat rendering, file upload
- `main.py` — Agent logic, prompt engineering, response parsing
- `tools.py` — Optional helper tools (search/wiki/save)
- `requirements.txt` — dependencies

## 🧱 Example requirements.txt

A typical dependency list (adjust versions as needed):

- streamlit
- langchain
- langchain-core
- langchain-google-genai
- langchain-community
- pydantic
- python-dotenv
- PyMuPDF
- python-docx
- duckduckgo-search
- wikipedia

Freeze exact versions:

```bash
pip freeze > requirements.txt
```

## 🧰 Troubleshooting

1. ModuleNotFoundError
   - Install missing dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. API key not set
   - Go to sidebar → paste Gemini key → click Save Key

3. RESOURCE_EXHAUSTED / 429
   - This means Gemini quota or rate limits were exceeded.
   - Wait and retry, or switch model, or upgrade tier.

4. 404 model not found
   - Use supported models: `gemini-2.5-flash-lite`, `gemini-2.5-flash`.

5. Old responses disappearing
   - Streamlit rerun can reset state. Use **Clear Chat** intentionally and rely on `st.session_state.chat_messages`.

6. PDF / DOCX not being read
   - Ensure uploaded file is valid, flickselectable text, supported format.
   - Scanned PDFs without OCR may fail.
