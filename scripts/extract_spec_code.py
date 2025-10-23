"""Utility for extracting code blocks from BizDocumentAI spec files.

This module reads Markdown or PDF spec documents and emits the fenced code
blocks they contain. It is designed primarily for `requirements.md` and
`requirements.pdf`, but works with any Markdown-like source that uses triple
backticks to delimit blocks.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional


BACKTICK_PATTERN = re.compile(r"^```(?P<lang>[^\n`]*)$", re.MULTILINE)


@dataclass
class CodeBlock:
    """Representation of a fenced code block in a spec document."""

    language: Optional[str]
    content: str
    source: Path
    start_line: int

    def to_json(self) -> dict:
        return {
            "language": self.language,
            "content": self.content,
            "source": str(self.source),
            "start_line": self.start_line,
        }


def read_markdown(path: Path) -> str:
    """Load a Markdown file as UTF-8 text."""

    return path.read_text(encoding="utf-8")


def read_pdf(path: Path) -> str:
    """Extract textual content from a PDF file.

    The function prefers the `pypdf` package but will fall back to `PyPDF2`
    if necessary. A meaningful error is raised when neither dependency is
    available.
    """

    try:
        from pypdf import PdfReader  # type: ignore
    except ModuleNotFoundError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ModuleNotFoundError as exc:  # pragma: no cover - exercised in runtime
            raise RuntimeError(
                "Either 'pypdf' or 'PyPDF2' must be installed to parse PDF specs."
            ) from exc

    reader = PdfReader(str(path))
    pages: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def iter_code_blocks(text: str, *, source: Path) -> Iterator[CodeBlock]:
    """Yield `CodeBlock` instances for the given document text."""

    in_block = False
    language: Optional[str] = None
    buffer: List[str] = []
    start_line = 0

    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        if not in_block:
            match = BACKTICK_PATTERN.match(line.strip())
            if match:
                in_block = True
                lang_token = match.group("lang").strip()
                language = lang_token or None
                buffer = []
                start_line = idx + 1
            continue

        if line.strip() == "```":
            yield CodeBlock(
                language=language,
                content="\n".join(buffer).rstrip("\n"),
                source=source,
                start_line=start_line,
            )
            in_block = False
            language = None
            buffer = []
            start_line = 0
            continue

        buffer.append(line)

    # Handle unterminated blocks gracefully by emitting the buffered content.
    if in_block and buffer:
        yield CodeBlock(
            language=language,
            content="\n".join(buffer).rstrip("\n"),
            source=source,
            start_line=start_line,
        )


def extract_from_file(path: Path) -> List[CodeBlock]:
    """Extract code blocks from a Markdown or PDF file."""

    suffix = path.suffix.lower()
    if suffix == ".md":
        text = read_markdown(path)
    elif suffix == ".pdf":
        text = read_pdf(path)
    else:
        raise ValueError(f"Unsupported spec format: {path}")

    return list(iter_code_blocks(text, source=path))


def extract_many(paths: Iterable[Path]) -> List[CodeBlock]:
    blocks: List[CodeBlock] = []
    for path in paths:
        blocks.extend(extract_from_file(path))
    return blocks


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract fenced code blocks from BizDocumentAI spec files."
    )
    parser.add_argument(
        "paths",
        metavar="SPEC",
        type=Path,
        nargs="+",
        help="Path(s) to Markdown or PDF spec files.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of a human-readable listing.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    blocks = extract_many(args.paths)

    if args.json:
        print(json.dumps([block.to_json() for block in blocks], indent=2))
    else:
        for block in blocks:
            header = f"{block.source} (line {block.start_line})"
            if block.language:
                header += f" [{block.language}]"
            print(header)
            print("-" * len(header))
            print(block.content)
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
