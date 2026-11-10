import sys
from pathlib import Path

from analyzer import check


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        ok, message = check(line)
        print(f"{number}. {line!r}: {'OK' if ok else 'ERROR'}")
        if not ok:
            print("   " + message.replace("\n", "\n   "))


if __name__ == "__main__":
    main()
