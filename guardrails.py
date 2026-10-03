MAX_LOG_LENGTH = 12000

DEVOPS_KEYWORDS = [
    "kubernetes",
    "pod",
    "docker",
    "terraform",
    "aws",
    "s3",
    "iam",
    "ec2",
    "database",
    "postgres",
    "mysql",
    "github actions",
    "ci/cd",
    "deployment",
    "container",
    "linux",
    "error",
    "exception",
    "timeout",
    "failed",
]


def validate_input(log_text: str) -> tuple[bool, str]:
    """
    Validate the incident log before analysis.
    """

    # Check 1: Empty input
    if not log_text or not log_text.strip():
        return False, "Please provide an incident log."

    # Check 2: Excessively large input
    if len(log_text) > MAX_LOG_LENGTH:
        return False, (
            f"Log is too long. Maximum allowed length is "
            f"{MAX_LOG_LENGTH} characters."
        )

    # Check 3: Basic DevOps/application scope check
    text = log_text.lower()

    if not any(keyword in text for keyword in DEVOPS_KEYWORDS):
        return False, (
            "This does not appear to be a DevOps or application incident log. "
            "Please provide a relevant technical log."
        )

    return True, ""


REQUIRED_SECTIONS = [
    "### Incident Summary",
    "### Likely Cause",
    "### Evidence",
    "### Severity",
    "### Recommended Checks",
]


def validate_output(response: str) -> tuple[bool, str]:
    """
    Check whether the analysis contains all required sections.
    """

    if not response or not response.strip():
        return False, "The analysis returned an empty response."

    missing_sections = [
        section
        for section in REQUIRED_SECTIONS
        if section not in response
    ]

    if missing_sections:
        return False, (
            "The analysis is missing required sections: "
            + ", ".join(missing_sections)
        )

    return True, ""