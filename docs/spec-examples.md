# BizDocumentAI Specification Examples

The fixtures below transcribe every sample from `requirements.pdf` so tests can assert parser behaviour directly against the canonical
scenarios. Each example lists the original BizDocumentAI input alongside the expected JSON structure.

## Empty text
- Input fixture: `tests/fixtures/empty-text.input.txt`
- Output fixture: `tests/fixtures/empty-text.output.json`

_Input_
```
```

_Output_
```json
{
  "kind": "block"
}
```

## Body paragraphs
- Input fixture: `tests/fixtures/body-basic.input.txt`
- Output fixture: `tests/fixtures/body-basic.output.json`

_Input_
```
First paragraph.

Second paragraph.
```

_Output_
```json
{
  "kind": "block",
  "body": [
    "First paragraph.",
    "Second paragraph."
  ]
}
```

## Body paragraphs with extra blank lines
- Input fixture: `tests/fixtures/body-skip-blank.input.txt`
- Output fixture: `tests/fixtures/body-skip-blank.output.json`

_Input_
```
First paragraph.


Second paragraph.
```

_Output_
```json
{
  "kind": "block",
  "body": [
    "First paragraph.",
    "Second paragraph."
  ]
}
```

## Head tag
- Input fixture: `tests/fixtures/head.input.txt`
- Output fixture: `tests/fixtures/head.output.json`

_Input_
```
<head>Test Document</head>
Content
```

_Output_
```json
{
  "kind": "block",
  "head": "Test Document",
  "body": [
    "Content"
  ]
}
```

## Nested blocks
- Input fixture: `tests/fixtures/blocks-nested.input.txt`
- Output fixture: `tests/fixtures/blocks-nested.output.json`

_Input_
```
<head>AI Coding Kata</head>
Let's get started with the kata
<block>

<head>Preface</head>

Here is a little story
</block>
```

_Output_
```json
{
  "kind": "block",
  "head": "AI Coding Kata",
  "body": [
    "Let's get started with the kata",
    {
      "kind": "block",
      "head": "Preface",
      "body": [
        "Here is a little story"
      ]
    }
  ]
}
```

## Dictionary (default separator)
- Input fixture: `tests/fixtures/dict-default.input.txt`
- Output fixture: `tests/fixtures/dict-default.output.json`

_Input_
```
<dict sep=":">
Key One: Value One
Key Two: Value Two
Key Three: Value Three
</dict>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "dict",
      "items": {
        "Key One": "Value One",
        "Key Two": "Value Two",
        "Key Three": "Value Three"
      }
    }
  ]
}
```

## Dictionary (custom separator and empty value)
- Input fixture: `tests/fixtures/dict-custom.input.txt`
- Output fixture: `tests/fixtures/dict-custom.output.json`

_Input_
```
<dict sep="-">
Title - AI Coding - for TAT
Kata Number -
</dict>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "dict",
      "items": {
        "Title": "AI Coding - for TAT",
        "Kata Number": ""
      }
    }
  ]
}
```

## Ordered list
- Input fixture: `tests/fixtures/list-ordered.input.txt`
- Output fixture: `tests/fixtures/list-ordered.output.json`

_Input_
```
<list kind=".">
1. First

2. Second
</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "1.",
          "head": "First"
        },
        {
          "kind": "block",
          "number": "2.",
          "head": "Second"
        }
      ]
    }
  ]
}
```

## Ordered list with nested numbering
- Input fixture: `tests/fixtures/list-ordered-nested.input.txt`
- Output fixture: `tests/fixtures/list-ordered-nested.output.json`

_Input_
```
<list kind=".">
1. First

2. Second

2.1. Subitem 1
2.2. Subitem 2
</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "1.",
          "head": "First"
        },
        {
          "kind": "block",
          "number": "2.",
          "head": "Second",
          "body": [
            {
              "kind": "list",
              "items": [
                {
                  "kind": "block",
                  "number": "2.1.",
                  "head": "Subitem 1"
                },
                {
                  "kind": "block",
                  "number": "2.2.",
                  "head": "Subitem 2"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Unordered list
- Input fixture: `tests/fixtures/list-unordered.input.txt`
- Output fixture: `tests/fixtures/list-unordered.output.json`

_Input_
```
<list kind="*">
* First
* Second
* Third
</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "*",
          "head": "First"
        },
        {
          "kind": "block",
          "number": "*",
          "head": "Second"
        },
        {
          "kind": "block",
          "number": "*",
          "head": "Third"
        }
      ]
    }
  ]
}
```

## Unordered list with nested `o`
- Input fixture: `tests/fixtures/list-unordered-nested.input.txt`
- Output fixture: `tests/fixtures/list-unordered-nested.output.json`

_Input_
```
<list kind="*">
* First
o Subitem
* Second
* Third
</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "*",
          "head": "First",
          "body": [
            {
              "kind": "list",
              "items": [
                {
                  "kind": "block",
                  "number": "o",
                  "head": "Subitem"
                }
              ]
            }
          ]
        },
        {
          "kind": "block",
          "number": "*",
          "head": "Second"
        },
        {
          "kind": "block",
          "number": "*",
          "head": "Third"
        }
      ]
    }
  ]
}
```

## Mixed lists
- Input fixture: `tests/fixtures/list-mixed.input.txt`
- Output fixture: `tests/fixtures/list-mixed.output.json`

_Input_
```
<list kind=".">
1. Beginning

2. Main
<list kind="*">
* Bullet 1
* Bullet 2
</list>

3. Ending
</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "1.",
          "head": "Beginning"
        },
        {
          "kind": "block",
          "number": "2.",
          "head": "Main",
          "body": [
            {
              "kind": "list",
              "items": [
                {
                  "kind": "block",
                  "number": "*",
                  "head": "Bullet 1"
                },
                {
                  "kind": "block",
                  "number": "*",
                  "head": "Bullet 2"
                }
              ]
            }
          ]
        },
        {
          "kind": "block",
          "number": "3.",
          "head": "Ending"
        }
      ]
    }
  ]
}
```

## Lists with additional content
- Input fixture: `tests/fixtures/list-with-content.input.txt`
- Output fixture: `tests/fixtures/list-with-content.output.json`

_Input_
```
<list kind=".">

1. First

First body

2. Second

Some more text

<dict sep=":">
Key: Value
Another Key: Another Value
</dict>

</list>
```

_Output_
```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        {
          "kind": "block",
          "number": "1.",
          "head": "First",
          "body": [
            "First body"
          ]
        },
        {
          "kind": "block",
          "number": "2.",
          "head": "Second",
          "body": [
            "Some more text",
            {
              "kind": "dict",
              "items": {
                "Key": "Value",
                "Another Key": "Another Value"
              }
            }
          ]
        }
      ]
    }
  ]
}
```
