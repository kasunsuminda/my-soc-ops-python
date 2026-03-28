---
applyTo: "**"
---

# Setup Instructions

## Purpose
Provide consistent local setup guidance and `setup` command intent for this repo.

## Usage
- Use `/setup` to instruct the agent to perform environment setup steps.
- This task should be idempotent and friendly for new contributors.

## Behavior
1. Locate and honor project README and docs, especially `README.md` and `docs/`.
2. Use Python venv in `.venv`, not system Python (unless containerized).
3. Install pin dependencies from `requirements.txt` or `pyproject.toml`.
4. Run tests with `pytest` in the repository root.
5. Avoid making network or external side-effect commands unless requested.

## Responses
- If asked "How do I set up?", reply with command sequence:
  - `cd /home/kasun-kariyakarawana/Desktop/dev days/my-soc-ops-python`
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -U pip`
  - `pip install -r requirements.txt` (or `pip install .` if poetry)
  - `pytest`
- If dependencies are missing, add a helpful check:
  - `ls requirements.txt pyproject.toml`
  - `cat README.md | sed -n '1,120p'`

## Keep It Safe
- Do not run destructive shell commands (`rm -rf`, `sudo apt-get remove`) unless explicitly approved.
- Suggest dry-run or confirmation for database/migration actions.
