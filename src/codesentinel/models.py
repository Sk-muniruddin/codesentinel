from pydantic import BaseModel, Field


class ReviewFinding(BaseModel):
    severity: str = Field(
        description="Severity: CRITICAL, HIGH, MEDIUM, LOW, or INFO"
    )
    file: str
    line: int | None = None
    category: str
    problem: str
    impact: str
    recommendation: str


class CodeReview(BaseModel):
    findings: list[ReviewFinding]
    summary: str
    overall_status: str = "PENDING"


def calculate_status(findings: list[ReviewFinding]) -> str:
    if not findings:
        return "PASSED"

    blocking_severities = {"CRITICAL", "HIGH", "MEDIUM"}

    for finding in findings:
        if finding.severity.upper() in blocking_severities:
            return "CHANGES_REQUESTED"

    return "PASSED"
# webhook event test

# webhook test
