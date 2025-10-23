import unittest
from pathlib import Path
from unittest import mock

from scripts.extract_spec_code import extract_from_file, iter_code_blocks


class CodeBlockExtractionTests(unittest.TestCase):
    def test_iter_code_blocks_parses_language_and_content(self) -> None:
        text = """\
Intro
```python
print('hello')
```
"""

        blocks = list(iter_code_blocks(text, source=Path("sample.md")))

        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertEqual(block.language, "python")
        self.assertEqual(block.content, "print('hello')")
        self.assertEqual(block.start_line, 3)

    def test_extract_from_markdown_spec_finds_known_block(self) -> None:
        spec_path = Path("requirements.md")

        blocks = extract_from_file(spec_path)

        self.assertGreater(len(blocks), 0)
        first = blocks[0]
        self.assertEqual(first.language, "python")
        self.assertIn("class Dictionary", first.content)

    def test_extract_from_pdf_uses_reader(self) -> None:
        spec_path = Path("requirements.pdf")

        with mock.patch(
            "scripts.extract_spec_code.read_pdf", return_value="```text\nvalue\n```"
        ) as mocked_reader:
            blocks = extract_from_file(spec_path)

        mocked_reader.assert_called_once_with(spec_path)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].content, "value")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
