from dataclasses import dataclass
import re


@dataclass
class ChangedLine:
    file: str
    line: int
    change_type: str
    content: str


def parse_git_diff(diff: str) -> list[ChangedLine]:
    results: list[ChangedLine] = []

    current_file: str | None = None
    new_line_number: int | None = None

    pending_deletions: list[str] = []

    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current_file = line.split(" ")[3][2:]
            new_line_number = None
            pending_deletions = []

        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)

            if match:
                new_line_number = int(match.group(1))

            pending_deletions = []

        elif line.startswith("+++ ") or line.startswith("--- "):
            continue

        elif line.startswith("\\"):
            # Git metadata such as:
            # \ No newline at end of file
            continue

        elif line.startswith("-"):
            pending_deletions.append(line[1:])

        elif line.startswith("+"):
            content = line[1:]

            # Ignore blank added lines.
            if content == "":
                if new_line_number is not None:
                    new_line_number += 1
                continue

            # Ignore a deletion/addition pair when the content is identical.
            if content in pending_deletions:
                pending_deletions.remove(content)

            elif current_file is not None and new_line_number is not None:
                results.append(
                    ChangedLine(
                        file=current_file,
                        line=new_line_number,
                        change_type="added",
                        content=content,
                    )
                )

            if new_line_number is not None:
                new_line_number += 1

        else:
            # Flush genuine deletions before moving past the hunk line.
            for deleted_content in pending_deletions:
                results.append(
                    ChangedLine(
                        file=current_file or "",
                        line=0,
                        change_type="deleted",
                        content=deleted_content,
                    )
                )

            pending_deletions = []

            if new_line_number is not None:
                new_line_number += 1

    # Flush remaining genuine deletions.
    for deleted_content in pending_deletions:
        results.append(
            ChangedLine(
                file=current_file or "",
                line=0,
                change_type="deleted",
                content=deleted_content,
            )
        )

    return results