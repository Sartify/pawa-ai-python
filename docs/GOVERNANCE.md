# Repository governance

This guide explains how to restrict who can change `main`, who can merge code, and who can publish to PyPI — even though the repository is **public**.

> **Public repo ≠ open merge access.** Anyone can *view* and *fork* the code. Only people you grant permissions can push, merge, or release.

## Recommended roles

Create a GitHub team named **Pawa** under the **Sartify** organization (if it does not exist yet).

| Role | GitHub permission | Who |
|------|-------------------|-----|
| Maintainers | **Maintain** or **Admin** | Core Sartify SDK team (2–5 people) |
| Trusted contributors | **Write** | Regular internal contributors |
| Everyone else | None (fork + PR) | Community, contractors, experiments |

**Do not** give **Admin** to everyone. Keep Admin to 1–2 people who manage org settings and branch protection.

### What each permission allows

| Permission | Clone / fork | Open PR | Push feature branch | Merge to `main` | Create releases | Change branch rules |
|------------|--------------|---------|---------------------|-----------------|-----------------|---------------------|
| None (public) | Yes | Yes (from fork) | No | No | No | No |
| Write | Yes | Yes | Yes* | Only if rules allow | No | No |
| Maintain | Yes | Yes | Yes* | Only if rules allow | Yes | Some settings |
| Admin | Yes | Yes | Yes* | Only if rules allow | Yes | Yes |

\*Even with Write/Maintain, **branch protection** can block direct pushes to `main`.

## Step 1 — Protect the `main` branch

In GitHub: **Settings → Branches → Add branch protection rule** (or **Rules → Rulesets**).

Apply to branch: `main`

Enable:

- [x] **Require a pull request before merging**
  - Require approvals: **1** (use **2** for extra safety)
  - [x] **Require review from Code Owners** (uses `.github/CODEOWNERS`)
  - [x] Dismiss stale pull request approvals when new commits are pushed
- [x] **Require status checks to pass before merging**
  - Required checks: `Lint`, `Test (Python 3.12)`, `Build package` (names from CI workflow)
- [x] **Require branches to be up to date before merging**
- [x] **Do not allow bypassing the above settings** (or limit bypass to org owners only)
- [x] **Restrict who can push to matching branches** → select **Pawa** only  
  (Everyone else must use PRs; most external contributors use forks anyway.)
- [x] **Block force pushes**
- [x] **Block branch deletion**

### Create the team + CODEOWNERS

1. Org **Settings → Teams** → open or create the **Pawa** team
2. Add core maintainers to the team
3. This repo includes `.github/CODEOWNERS` pointing at `@Sartify/Pawa`

## Step 2 — Contribution workflow (external people)

For people **outside** the maintainer team:

1. They **fork** the public repo (no write access to yours)
2. Push changes to **their fork**
3. Open a **Pull Request** into `main`
4. CI runs automatically on the PR
5. A **code owner** must approve
6. A maintainer merges

They never get direct push access to `main` unless you explicitly invite them with Write access **and** your branch rules still require PR + review.

## Step 3 — Lock down PyPI publishing

Publishing is the highest-risk action. Use **two layers**:

### A. GitHub Environment (`pypi`)

**Settings → Environments → New environment** → name: `pypi`

Configure:

- [x] **Required reviewers** → add **Pawa** (1–2 people must approve each deploy)
- **Deployment branches** → **Selected branches and tags** → allow only release tags, e.g. `v*`  
  Or restrict to tags matching semver: `v*.*.*`

The publish workflow (`.github/workflows/publish.yml`) already targets this environment. A release alone is **not enough** — a maintainer must approve the deployment job.

### B. PyPI Trusted Publishing

On PyPI, configure Trusted Publishing for:

- **Repository**: `Sartify/pawa-ai-python`
- **Workflow**: `publish.yml`
- **Environment**: `pypi` (recommended — scopes token to that environment only)

This ensures only that specific workflow + environment can upload packages, even if someone steals a generic token (Trusted Publishing uses short-lived OIDC tokens, no long-lived PyPI password in GitHub Secrets).

### C. Tag format guard

The publish workflow only runs for semver tags like `v0.2.0` to avoid accidental publishes from malformed releases.

## Step 4 — GitHub Actions permissions

**Settings → Actions → General**

- **Workflow permissions**: **Read repository contents** (default minimal)
- Do **not** enable "Read and write" globally unless a workflow needs it
- Our publish workflow requests only `id-token: write` for OIDC to PyPI

For PRs from forks:

- Use **Require approval for all outside collaborators** (Settings → Actions → Fork pull request workflows)

This prevents untrusted PR code from running workflows with secrets until a maintainer approves the workflow run.

## Step 5 — Optional hardening

| Control | Purpose |
|---------|---------|
| Signed commits required | Verify commit authorship |
| Dependabot security updates | Auto PRs for vulnerable deps (still need review) |
| Secret scanning | Block accidental API keys in commits |
| `gh api` rulesets | Encode branch rules as code (org feature) |

## Quick setup with GitHub CLI

After `gh auth login` and creating the repo:

```bash
# Example: branch protection (adjust team slug)
gh api repos/Sartify/pawa-ai-python/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Lint","Test (Python 3.12)","Build package"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"require_code_owner_reviews":true}' \
  --field restrictions='{"users":[],"teams":["Pawa"],"apps":[]}' \
  --field required_linear_history=false \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

Create the `pypi` environment and required reviewers in the GitHub UI (environments are easier there than CLI).

## Summary

| Concern | Control |
|---------|---------|
| Random people changing `main` | Branch protection + required PR + CODEOWNERS |
| Random people merging PRs | Required approvals from code owners |
| Broken code merging | Required CI status checks |
| Unauthorized PyPI upload | `pypi` environment reviewers + Trusted Publishing + tag guard |
| Malicious PR workflows | Approve fork PR workflows before CI runs |

Public visibility helps adoption. **Branch protection, CODEOWNERS, and the `pypi` environment** keep release authority with your team.
