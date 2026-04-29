# Security Policy

## Reporting a vulnerability

**Please don't open a public issue for security vulnerabilities.**

Instead, report them privately via GitHub's private vulnerability reporting:

👉 [Open a security advisory](https://github.com/NiklasTiede/Github-Trending-API/security/advisories/new)

This keeps the report visible only to the maintainers until a fix is ready.

### What to include

- A clear description of the vulnerability.
- Steps to reproduce, or a proof-of-concept if possible.
- The affected version(s) — ideally a commit SHA or release tag.
- The impact you think it has (data exposure, RCE, DoS, etc.).

### What to expect

This is a maintained side project, so timelines are best-effort:

- **Acknowledgement:** within 7 days.
- **Initial assessment:** within 14 days.
- **Fix or mitigation:** depends on severity and complexity.

Once a fix is released, you'll be credited in the release notes unless you'd prefer to stay anonymous.

## Supported versions

Only the latest released version on the `main` branch receives security updates. If you're running an older version, please upgrade before reporting — the issue may already be fixed.

| Version | Supported |
| ------- | --------- |
| Latest release on `main` | ✅ |
| Older releases | ❌ |

## Scope

In scope:

- The API code in this repository (`app/`).
- The published Docker image (`niklastiede/github-trending-api`).
- Dependencies pinned in `uv.lock` (please report upstream too, where applicable).

Out of scope:

- Vulnerabilities in GitHub's trending page itself — report those to GitHub.
- Issues that only affect forks or unsupported deployment configurations.
- Rate-limiting or abuse of the upstream `github.com/trending` page.
