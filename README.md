# 🧾 SmartReceipt

## 📑 Contents

- 📝 Description
- 🗺️ Roadmap
- 🛠️ Tech Stack used
- 🎥 Demo
- 📚 Resources
- 
- 💬Commit guidelines


## 📝 Description



## 🗺️ Roadmap
## 🛠️ Tech Stack used
## 🎥 Demo
## 📚 Resources

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
