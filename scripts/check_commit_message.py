import re
import sys


COMMIT_PATTERN = re.compile(
    r"^(feat|fix|docs|refactor|test|chore|init)\([a-z0-9_-]+\): .+$"
)


def main() -> int:
    commit_message_file = sys.argv[1]

    with open(commit_message_file, encoding="utf-8") as file:
        message = file.readline().strip()

    if not COMMIT_PATTERN.match(message):
        print(
            "Invalid commit message.\n"
            "Expected format: <type>(<scope>): <short_description>\n"
            "Allowed types: feat, fix, docs, refactor, test, chore\n"
            "Example: feat(auth): add login endpoint"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
