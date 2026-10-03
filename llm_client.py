import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:1.7b"


SYSTEM_PROMPT = """
You are a DevOps incident-analysis assistant.

Analyze only the technical log supplied by the user.

Return exactly these five sections:

### Incident Summary
Briefly summarize what happened.

### Likely Cause
Explain the most likely cause. Clearly distinguish a hypothesis from confirmed evidence.

### Evidence
List the specific facts from the supplied log that support the analysis.

### Severity
Classify the incident as Low, Medium, or High and briefly explain why.

### Recommended Checks
Give practical, non-destructive troubleshooting checks an engineer can perform.

Rules:
- Do not invent facts that are not present in the log.
- If there is insufficient information, explicitly say so.
- Distinguish evidence from hypotheses.
- Do not recommend destructive production actions.
- Stay within DevOps/application incident troubleshooting.
"""


def analyze_log(log_text: str) -> str:
    """
    Send the incident log to the local Ollama LLM.
    """

    prompt = f"""
{SYSTEM_PROMPT}

Incident log:

{log_text}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read().decode("utf-8"))

        result = data.get("response", "").strip()

        if not result:
            raise RuntimeError("Ollama returned an empty response.")

        # Remove Qwen3 reasoning if it appears before the final answer.
        if "</think>" in result:
            result = result.split("</think>", 1)[1].strip()

        return result

    except Exception as exc:
        raise RuntimeError(
            f"Could not connect to the local Ollama model. "
            f"Make sure Ollama is running and the model "
            f"'{MODEL_NAME}' is available. Details: {exc}"
        )