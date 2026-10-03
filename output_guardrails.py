DANGEROUS_PATTERNS = [
    "delete production",
    "drop database",
    "drop table",
    "terminate production",
    "terminate instance",
    "force delete",
    "rm -rf",
    "terraform destroy",
]


def check_recommendations(response: str) -> tuple[bool, list[str]]:
    """
    Check AI recommendations for potentially destructive actions.
    """

    response_lower = response.lower()

    warnings = [
        pattern
        for pattern in DANGEROUS_PATTERNS
        if pattern in response_lower
    ]

    if warnings:
        return False, warnings

    return True, []