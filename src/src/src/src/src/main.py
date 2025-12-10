import argparse
import json
import sys
from pathlib import Path

from .extractor import extract_entities_from_text


def main():
    parser = argparse.ArgumentParser(
        description="Financial News Entity Extraction using Gen AI"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Path to a text file containing news article"
    )
    parser.add_argument(
        "-o", "--out", type=str, help="Optional path to save JSON output", default=None
    )
    parser.add_argument(
        "-m", "--model", type=str, help="Model name", default="gpt-4.1-mini"
    )

    args = parser.parse_args()

    if args.file:
        text_path = Path(args.file)
        if not text_path.exists():
            print(f"File not found: {text_path}", file=sys.stderr)
            sys.exit(1)
        text = text_path.read_text(encoding="utf-8")
    else:
        print("Reading text from stdin. Press Ctrl+D (Linux/macOS) or Ctrl+Z (Windows) to end input.")
        text = sys.stdin.read()

    entities = extract_entities_from_text(text, model=args.model)
    json_str = json.dumps(entities, indent=2, ensure_ascii=False)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"✅ Saved entities to {out_path}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
