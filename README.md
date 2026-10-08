# 🧾 SmartReceipt

## 📑 Contents

- 📝 Description
- 🗺️ Roadmap
- 🛠️ Tech Stack used
- 🎥 Demo
- 📚 Resources
- 🌿 Branch Naming Guidelines
- 💬Commit guidelines


## 📝 Description
## 🗺️ Roadmap

### Milestone 1 - OCR

Input: 

```commandline
receipt.jpg
```

Output: 
```commandline
KAUFLAND
14.03.2026
LAPTE 7.49
PAINE 4.99
TOTAL 12.48
```

### Milestone 2 - Image Preprocessing

```commandline
  Photo
    |
  Rotate
    |
  Crop
    |
  Resize
    |
  Grayscale
    | 
  Denoise
    | 
  Contrast / Threshold
    | 
   OCR
```

We can make the following comparison here:

```commandline
original image -> OCR accuracy
        vs
preprocessed image -> accuracy
```
### Milestone 3 - OCR Data Model

Transform the OCR result into a Python data model.

```python
[
  {
    "text": "LAPTE",
    "confidence": 0.97,
    "box": [120, 340, 250, 375]
  },
  {
    "text": "7.49",
    "confidence": 0.95,
    "box": [500, 340, 570, 375]
  }
]
```

### Milestone 4 - Receipt parser

Create the JSON output using a deterministic, rule-based parser.

```json
{
  "merchant": "KAUFLAND",
  "date": "2026-03-14",
  "items": [
    {
      "name": "LAPTE",
      "quantity": 1,
      "unit_price": 7.49,
      "total_price": 7.49
    },
    {
      "name": "PAINE",
      "quantity": 1,
      "unit_price": 4.99,
      "total_price": 4.99
    }
  ],
  "total": 12.48,
  "currency": "RON"
}
```

### Milestone 5 - Receipt schema

Define the structure of a receipt using a Python data model:

```
Receipt
├── merchant
├── date
├── time
├── currency
├── items
│   ├── name
│   ├── quantity
│   ├── unit_price
│   └── total_price
└── total
```

### Milestone 6 - Validation

Here we check if the result makes sense:

```
7.49
4.99
─────
12.48
```

And we can also check: 

```
date valid?
total valid?
prices positive?
currency valid?
confidence suficient?
```

### Milestone 7 - AI

This milestone will add an AI-based parser/extractor which will replace or enhance the logic from Milestone 4

`Scope`: We will build first a deterministic solution, then we introduce AI and compare the results. 

## 🛠️ Tech Stack used
## 🎥 Demo
## 📚 Resources

## 🌿 Branch Naming Guidelines

This project follows a consistent branch naming convention:

```<type>/<short-description>```

### 🏷️ Branch types

- feat -- add a new feature
- fix -- fix a bug
- docs -- documentation changes
- refactor -- code changes that do not add features or fix bugs
- test -- add or modify tests
- chore -- maintenance tasks, dependencies, configuration, etc.

### 💡 Examples

```commandline
feat/receipt-ocr 
feat/image-preprocessing 
fix/empty-receipt 
fix/ocr-confidence 
docs/setup-guide 
refactor/receipt-parser 
test/receipt-parser 
chore/update-dependencies
```

### 📏 Rules

- `<type>` must be one of the types listed above.
- Use lowercase for the branch type and description.
- Separate words in `<short-description>` with hyphens `(-)`.
- Keep the description short and descriptive.
- Avoid unnecessary words or implementation details.
- Do not use spaces, underscores, or special characters in the branch name.

## 💬 Commit guidelines

This project follows a consistent commit message format:

`````<type>(<scope>): <short_description>`````

### 🏷️ Commit Types

- feat -- add a new feature
- fix -- fix a bug
- docs -- documentation changes
- refactor -- code changes that do not add features of fix bugs
- test -- add or modify tests
- chore -- maintenance tasks, dependencies, configuration, etc.
- init -- project initialization

### 💡 Examples

```commandline
feat(ocr): add receipt text extraction 
fix(parser): handle missing total 
docs(readme): add installation instructions 
refactor(ocr): simplify image preprocessing 
test(parser): add receipt parsing tests 
chore(deps): update dependencies 
init(project): initialize the project
```

### 📏 Rules

- `<type>` must be one of the types listed above
- `<scope>` should identify the component or area affected by the changes
- `<short_description>` should briefly describe the change
- Use lowercase for type and scope
- Keep description concise and descriptive

Commits that do not follow this format will be rejected automatically by the project's precommit hook.
