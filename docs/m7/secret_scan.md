# Secret scan before the repository goes public

Date: 2026-11-11. Spec, security: a pre-commit hook and a CI step (gitleaks) block any committed
secret. Before publishing, the whole history was scanned once.

| Check | Scope | Result |
| --- | --- | --- |
| gitleaks 8.30.1 (official image), `git` mode, `--all` | 51 commits, every branch, about 29.6 MB | no leaks found |
| The real AI key of the build environment, searched as a literal | every file of every commit | not found |
| Files named like secrets (`.env`, `secrets.toml`, keys, certificates) | every tracked file | none |
| GitHub Actions `secrets` job (same gitleaks scan) | on every push from now on | passed on its first run |

Keys are read from the environment only (`config/models.yaml` names the variable, never the
value); a key typed into the app is kept in memory and never written (M5 test).

**To rerun locally:**

```bash
docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:v8.30.1 git /repo --log-opts="--all" --redact
```
