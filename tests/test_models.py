from codesentinel.models import ReviewFinding, calculate_status


def make_finding(severity: str) -> ReviewFinding:
    return ReviewFinding(
        severity=severity,
        file="sample.py",
        line=10,
        category="Security",
        problem="Test problem",
        impact="Test impact",
        recommendation="Test recommendation",
    )


def test_empty_findings_pass():
    assert calculate_status([]) == "PASSED"


def test_low_finding_passes():
    findings = [make_finding("LOW")]

    assert calculate_status(findings) == "PASSED"


def test_medium_finding_requests_changes():
    findings = [make_finding("MEDIUM")]

    assert calculate_status(findings) == "CHANGES_REQUESTED"


def test_high_finding_requests_changes():
    findings = [make_finding("HIGH")]

    assert calculate_status(findings) == "CHANGES_REQUESTED"


def test_critical_finding_requests_changes():
    findings = [make_finding("CRITICAL")]

    assert calculate_status(findings) == "CHANGES_REQUESTED"


def test_mixed_findings_requests_changes():
    findings = [
        make_finding("LOW"),
        make_finding("MEDIUM"),
        make_finding("HIGH"),
    ]

    assert calculate_status(findings) == "CHANGES_REQUESTED"