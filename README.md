# 🛠️ AI DevOps Incident Assistant

A beginner-friendly Generative AI project for first-pass DevOps and application incident analysis.

The assistant takes a technical incident log and uses a local Large Language Model (LLM) to generate a structured analysis containing:

- Incident Summary
- Likely Cause
- Evidence
- Severity
- Recommended Checks

The project is designed as a practical example of applying Generative AI to a DevOps troubleshooting workflow.

## Why I built it

My background is in cloud infrastructure and DevOps, including AWS, Terraform, Kubernetes/EKS, CI/CD, monitoring, and troubleshooting.

I wanted to explore how an LLM could be used within a workflow I already understand, while also learning practical concepts such as prompt engineering, AI evaluation, guardrails, and human-in-the-loop review.

## Architecture

```text
User
  ↓
Streamlit Web Interface
  ↓
Input Guardrails
  ↓
Structured Prompt
  ↓
Local LLM (Ollama + Qwen3)
  ↓
Output Validation
  ↓
Safety / Recommendation Guardrail
  ↓
Structured Incident Analysis
```

## Technologies

- Python
- Streamlit
- Ollama
- Qwen3 1.7B
- Prompt Engineering
- Basic AI Guardrails
- Golden Test Set Evaluation
- Git / GitHub

## What it demonstrates

### 1. Generative AI / LLM integration

The project uses a local Qwen3 1.7B model through Ollama.

No external API key is required.

The LLM runs locally, making the project free to run once Ollama and the model are installed.

### 2. Prompt engineering

A structured system prompt instructs the model to:

- Analyze only the supplied technical log
- Return five predefined sections
- Distinguish evidence from hypotheses
- Avoid inventing facts
- State when information is insufficient
- Recommend non-destructive troubleshooting checks

### 3. Input guardrails

Before sending a log to the model, the application checks:

- Whether the input is empty
- Whether the input exceeds the maximum allowed length
- Whether the input appears relevant to DevOps/application troubleshooting

### 4. Output validation

The application checks whether the LLM response contains all required sections:

- Incident Summary
- Likely Cause
- Evidence
- Severity
- Recommended Checks

### 5. Safety guardrail

The project includes a lightweight recommendation safety check that detects potentially destructive actions such as:

- `terraform destroy`
- `rm -rf`
- `drop database`
- `terminate production`
- `delete production`

If a potentially destructive recommendation is detected, the application displays a warning so that an engineer can review it before taking action.

This is a lightweight human-in-the-loop safety mechanism, not a complete production safety system.

### 6. AI output evaluation

The project includes a small golden test set containing five synthetic incident scenarios:

1. Kubernetes CrashLoopBackOff
2. AWS S3 AccessDenied
3. Database Connection Timeout
4. CI/CD Docker Build Failure
5. Terraform IAM Policy Conflict

The evaluator checks whether the generated response contains expected concepts from each incident.

Current evaluation result:

```text
5/5 (100%)
```

The evaluation is intended as a simple demonstration of repeatable AI output testing rather than a comprehensive production evaluation framework.

## Example incident

Input:

```text
ERROR: Pod payment-service-7d8f9c failed to start
Status: CrashLoopBackOff
Readiness probe failed
Connection refused: 10.0.2.15:8080
```

The assistant produces a structured analysis covering the incident summary, probable cause, evidence, severity, and recommended troubleshooting checks.

## Running locally

### 1. Clone the repository

```bash
git clone https://github.com/ipsyy/ai-devops-incident-assistant.git
cd ai-devops-incident-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, the project can also be run directly using the Python executable inside `.venv`.

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Ollama

Install Ollama on your local machine and make sure the Ollama service is running.

### 6. Download the model

```bash
ollama pull qwen3:1.7b
```

### 7. Start the application

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Running the evaluation

The evaluation can also be run directly from the terminal:

```bash
python evaluator.py
```

The application also provides a **Run Evaluation Tests** button in the Streamlit interface.

## Project structure

```text
ai-devops-incident-assistant/
|
+-- app.py
+-- evaluator.py
+-- guardrails.py
+-- llm_client.py
+-- output_guardrails.py
+-- requirements.txt
+-- sample_data.py
+-- README.md
+-- .gitignore
```
