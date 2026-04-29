# Contributing

Thanks for considering a contribution! This project is small, so the process is intentionally lightweight.

## Before you start

- For **bug reports** and **feature requests**, open an [issue](https://github.com/NiklasTiede/Github-Trending-API/issues).
- For **questions, ideas, or general chat**, use [Discussions](https://github.com/NiklasTiede/Github-Trending-API/discussions).
- For **larger changes**, open an issue or discussion first to align on the approach before writing code. Saves you and me time.

## Local setup

You'll need [uv](https://docs.astral.sh/uv/) (the project uses Python 3.13, pinned in `.python-version`).

```bash
git clone https://github.com/NiklasTiede/Github-Trending-API.git
cd Github-Trending-API
uv sync --dev
```

Run the API locally:

```bash
make run
# or: uv run python -m uvicorn app.main:app --host 127.0.0.1 --port 1313 --reload
```

## Workflow

1. Fork the repo and create a branch off `main`.
2. Make your change. Keep commits focused.
3. Run the checks locally before pushing:

   ```bash
   make pre-commit   # ruff, formatting, etc.
   make test         # pytest with coverage
   ```

4. Push and open a pull request. Fill in the PR template.
5. CI runs the same checks plus a Docker build. Both must be green.

## Code style

- Linting and formatting are handled by `ruff` via pre-commit. Just run `make pre-commit` and you're good.
- Type hints are expected for new public functions and Pydantic models.
- Follow the patterns already in `app/` — adding a new endpoint should look like the existing ones.

## Tests

- New endpoints, parsers, or filters need tests in `tests/`.
- Aim to keep coverage from dropping. Bonus points if you raise it.
- Network-dependent tests should mock the upstream HTML response — no real calls to github.com/trending in the test suite.

## Commit messages

Loose convention based on [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add spoken_language_code filter to /developers
fix: handle missing avatar URLs in trending repos
docs: clarify Docker port in README
chore: bump fastapi to 0.115
```

This keeps the changelog readable and helps with release notes. Not strictly enforced but appreciated.

## Pull request expectations

- Small, focused PRs get reviewed faster than sprawling ones.
- Update `CHANGELOG.md` under `## [Unreleased]` if your change is user-visible.
- If you're touching the README or API surface, update the OpenAPI/Pydantic models too.

## Questions?

If anything in here is unclear, just ask in the [Discussions](https://github.com/NiklasTiede/Github-Trending-API/discussions). I'd rather you ask than get stuck.
