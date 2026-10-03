from llm_client import analyze_log


EVALUATION_CASES = [
    {
        "name": "Kubernetes CrashLoopBackOff",
        "log": """
ERROR: Pod payment-service-7d8f9c failed to start
Status: CrashLoopBackOff
Readiness probe failed
Connection refused: 10.0.2.15:8080
""",
        "required_concepts": [
            ["CrashLoopBackOff"],
            ["readiness probe"],
            ["8080"],
        ],
    },
    {
        "name": "AWS S3 AccessDenied",
        "log": """
ERROR: GetObject operation failed
AWS Error: AccessDenied
User is not authorized to perform s3:GetObject
Bucket: payments-prod
""",
        "required_concepts": [
            ["AccessDenied"],
            ["s3:GetObject"],
            ["payments-prod"],
        ],
    },
    {
        "name": "Database Connection Timeout",
        "log": """
ERROR: Database connection failed
Connection timed out after 30 seconds
Host: db-prod.internal
Port: 5432
""",
        "required_concepts": [
            ["timed out", "timeout"],
            ["db-prod.internal"],
            ["5432"],
        ],
    },
    {
        "name": "CI/CD Docker Build Failure",
        "log": """
ERROR: GitHub Actions deployment failed
Step: Docker Build
Error: failed to solve: npm install exited with code 1
""",
        "required_concepts": [
            ["Docker Build", "docker"],
            ["npm install"],
            ["code 1", "exit code 1"],
        ],
    },
    {
        "name": "Terraform IAM Policy Conflict",
        "log": """
Error: Error creating IAM policy
StatusCode: 409
EntityAlreadyExists
Policy named application-access already exists
""",
        "required_concepts": [
            ["IAM policy", "iam"],
            ["EntityAlreadyExists", "already exists"],
            ["409", "conflict"],
        ],
    },
]


def run_evaluation():
    total_cases = len(EVALUATION_CASES)
    passed_cases = 0

    print("\nAI DevOps Incident Assistant - Evaluation\n")
    print("=" * 55)

    for case in EVALUATION_CASES:
        result = analyze_log(case["log"])
        result_lower = result.lower()

        missing = []

        for concept_group in case["required_concepts"]:
            if not any(
                concept.lower() in result_lower
                for concept in concept_group
            ):
                missing.append(" / ".join(concept_group))

        if not missing:
            status = "PASS"
            passed_cases += 1
        else:
            status = "FAIL"

        print(f"\n{case['name']}")
        print(f"Result: {status}")

        if missing:
            print(f"Missing concepts: {', '.join(missing)}")

    score = (passed_cases / total_cases) * 100

    print("\n" + "=" * 55)
    print(f"Overall Score: {passed_cases}/{total_cases} ({score:.0f}%)")


if __name__ == "__main__":
    run_evaluation()