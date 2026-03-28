from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

# -----------------------------
# Default model
# -----------------------------
DEFAULT_MODEL = "gemini-2.5-flash-lite"

# -----------------------------
# Output schema
# -----------------------------
class TestStep(BaseModel):
    step: int = Field(description="Step number")
    action: str = Field(description="Action to perform")
    expected_result: str = Field(description="Expected result of the step")

class TestCaseResponse(BaseModel):
    test_case_id: str
    summary: str
    precondition: List[str]
    main_steps: List[TestStep]
    postcondition: List[str]
    sources: List[str]
    tools_used: List[str]

# -----------------------------
# Main runner
# -----------------------------
def run_research_agent(
    messages,
    api_key: str,
    model_name: str = DEFAULT_MODEL,
    attachment_text: str = "",
    attachment_description: str = ""
):
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key
    )

    system_prompt = """
You are an expert QA Test Case Generator for Advanced Therapies systems.

Domain Context:
Advanced Therapies utilizes X-ray technology primarily for image-guided interventional procedures
and radiation oncology rather than standalone diagnostic imaging.
This segment provides integrated robotic systems and angiography platforms designed to enable
minimally invasive treatments for conditions like cancer, including embolization for liver tumors
and cardiovascular intervention.

Your job:
Generate detailed, realistic, professional manual test cases from the user requirement.

Output Rules:
- Always generate exactly ONE structured test case.
- The response must strictly follow the structured schema.
- Make the test case practical, testable, and relevant to regulated medical workflow software.
- Include meaningful preconditions and postconditions.
- Main steps should be sequential, clear, and QA-friendly.
- Use realistic expected results.
- Generate a suitable test case ID based on the scenario.
- If attachment content is provided, use it as supporting context.
- If attachment description is provided, consider it as additional business/functional context.

Important:
- Do NOT invent random unrelated details.
- Do NOT return markdown.
- Do NOT return explanations outside the structured output.
"""

    # Build conversation text
    conversation_text = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if role == "user":
            conversation_text += f"User Requirement:\n{content}\n\n"
        elif role == "assistant":
            if isinstance(content, dict):
                conversation_text += f"Previous Generated Test Case:\n{content}\n\n"
            else:
                conversation_text += f"Assistant Response:\n{content}\n\n"

    attachment_block = ""
    if attachment_description.strip():
        attachment_block += f"\nAttachment Description:\n{attachment_description.strip()}\n"

    if attachment_text.strip():
        attachment_block += f"\nAttachment Extracted Content:\n{attachment_text.strip()[:15000]}\n"

    final_user_prompt = f"""
Generate a structured manual QA test case based on the following conversation and latest requirement.

{conversation_text}

{attachment_block}

Return only the structured output.
"""

    agent = create_agent(
        model=llm,
        tools=[],
        response_format=TestCaseResponse,
        system_prompt=system_prompt
    )

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": final_user_prompt}
        ]
    })

    if "structured_response" in response:
        return response["structured_response"]

    raise ValueError("Structured response not returned by the agent.")