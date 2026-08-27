from codesentinel.github_tools import get_pull_request_diff
from codesentinel.diff_parser import parse_git_diff


def test_parse_real_github_pr_diff():
    diff = get_pull_request_diff(
        "Sk-muniruddin",
        "codesentinel",
        1,
    )

    changes = parse_git_diff(diff)

    assert changes

    for change in changes:
        print(
            f"{change.file}:{change.line} "
            f"[{change.change_type}] {change.content}"
        )