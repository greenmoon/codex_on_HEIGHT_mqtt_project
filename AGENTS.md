# AGENTS.md

## Project instruction

This file gives Codex project-level guidance.  
Before analyzing, editing, or generating code, read and follow this file.

## Title Naming rule

if the titie as eg 'title_example V07 2026.06.24 17:32'
the version number should be added by one as 'V08'
the date should be changed as the today eg '2026.mm.dd hh:mm'    

## User abbreviation rules

The user often uses short abbreviation commands. Interpret them as task modifiers.

| Abbrev | Meaning |
|---|---|
| `tc` | Reply in Traditional Chinese. |
| `en` | Reply in English. |
| `dd` | Deep Dive, Give detailed explanation |
| `gg` | Generate Graphic, diagram, call tree, flow chart, or visual explanation when useful. |
| `nu` | NUmeric explain method in step by step present how the priciple explore|
| `ss` | Significant Summarize youtube, paper, source, screenshot, video, transcript, PDF, or provided text. |
| `ee` | Enhencement English, Improve the user's English sentence and provide a clearer version and english and chinese both  |
| `li` | Local Index html, Automatic run whole process built py->local html->auto open local index.html for checking
| `uu` | Upload URL, Automatic run whole process built py->html->push->repo project->world wide URL, auto open repo index.html for checking |
| `uunx` | Upload URL with number of x times 'y', Automatic run whole process built py->html->push->repo project->world wide URL, auto open repo index.html for checking |
| `uc xxxxxx` | Update Code to local, `authorized_code/code.txt` to `xxxxxx` in local folder only, commit, push to repo project, and open URL. Example: `uc 112358`. |
| `uc` | Update Code to repo, authorized code from local `authorized_code/code.txt`, commit, push, and open URL. local->repo|

## Interpretation examples

- `in tc`  
  → Reply in Traditional Chinese.

- `gg`  
  → Provide a call tree or flow diagram in picture form.

## Coding style preference

Prefer practical, minimal, easy-to-modify code.

When editing existing code:

1. Do not rewrite the whole project unless requested.
2. Preserve existing function names and data flow when possible.
3. Prefer small patches with clear insertion locations.
4. Explain why the change fixes the issue.
5. Avoid breaking existing behavior.
6. Add debug prints only when useful and removable.
7. Keep compatibility with Windows and Linux paths when possible.
8. Prefer relative paths over hard-coded absolute paths.
9. Use the same in PC folder name and in Github repo project name otherwise given WARN message 

## Project path style

Use cross-platform path handling.

Prefer:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent
csv_path = ROOT / "debug_inference" / "file.csv"
```

Avoid:

```python
csv_path = "C:\\Users\\..."
csv_path = "/home/user/..."
```

unless the user explicitly asks for physical absolute paths.

## Debug / analysis style

When checking bugs, report in this order:

1. Most likely root cause.
2. Evidence in code or log.
3. Minimal fix.
4. Safer long-term fix if needed.
5. Test method.
 
## Response style

Unless the user asks otherwise:

- Be direct.
- Prefer engineering explanation.
- Use tables for mappings.
- Use call trees for flow.
- Use concise comments in code.
- If user writes `tc`, answer in Traditional Chinese.
- If user writes `dd`, provide deeper detail.
