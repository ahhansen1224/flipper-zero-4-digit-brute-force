# =========================================
# file: build_payload_versioned.py
# Purpose: Generate DuckyScript v1.0 payloads with incrementing version numbers
# Run: python build_payload_versioned.py [-n COUNT] [--base-name NAME] [--out DIR]
# =========================================
from __future__ import annotations

import argparse
import random
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a DuckyScript v1.0 payload of random 4-digit codes, saved to Desktop with auto-incrementing version.",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=100,
        help="How many random 4-digit codes to generate (default: 100).",
    )
    parser.add_argument(
        "--base-name",
        type=str,
        default="notepad_100_codes",
        help="Base filename used before _vN suffix (default: notepad_100_codes).",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=str(Path.home() / "Desktop"),
        help="Output directory (default: your Desktop).",
    )
    return parser.parse_args()


def get_next_version_path(base_name: str, out_dir: Path) -> Path:
    """Return a Path like <out>/<base_name>_vN.txt with N = last+1."""
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = list(out_dir.glob(f"{base_name}_v*.txt"))

    max_ver = 0
    for f in existing:
        m = re.search(r"_v(\d+)\.txt$", f.name)
        if m:
            try:
                max_ver = max(max_ver, int(m.group(1)))
            except ValueError:
                pass

    next_ver = max_ver + 1
    return out_dir / f"{base_name}_v{next_ver}.txt"


def write_ducky_v1(file_path: Path, count: int) -> None:
    """Write header + COUNT unique 4-digit codes as DuckyScript v1.0."""
    if count > 10000:
        raise ValueError("Cannot generate more than 10,000 unique 4-digit codes.")

    header = (
        "REM =========================================\n"
        "REM Auto-generated random codes for Flipper Zero\n"
        "REM Compatible with legacy DuckyScript v1.0\n"
        "REM =========================================\n"
        "DELAY 400\n"
        "DEFAULT_DELAY 200\n\n"
    )

    # Ensure uniqueness by sampling without replacement
    codes = random.sample(range(0, 10000), count)

    with file_path.open("w", encoding="utf-8") as f:
        f.write(header)
        for code in codes:
            f.write(f"STRING {code:04}\n")
            f.write("ENTER\n")


def main() -> None:
    args = parse_args()

    if args.count <= 0:
        raise SystemExit("--count must be a positive integer")

    out_dir = Path(args.out).expanduser().resolve()
    target = get_next_version_path(args.base_name, out_dir)
    write_ducky_v1(target, args.count)
    print(f"✅ Fresh payload saved: {target}")


if __name__ == "__main__":
    main()
