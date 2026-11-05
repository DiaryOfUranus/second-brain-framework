# Security & Disclosure Notes

## Known historical exposure (disclosed, retained by design)

An external security review (November 2026) correctly identified that **older
commits** of this repository (prior to `288463d`) contained a hard-coded scrub
mapping inside `tools/scrub.py`, referencing the maintainer's instance name,
collaborator codenames, and local absolute paths of the development machine.

**Current status:**

- **Current tree and all release archives `v0.3.6+` are clean.** Since
  `288463d`, the scrub mapping is loaded from an external, git-ignored
  `tools/scrub_local.json` (see `tools/scrub_local.example.json`); missing
  config causes a fail-closed exit instead of a silent no-op scrub.
- **Git history is intentionally NOT rewritten.** We chose transparency over
  history scrubbing: the affected values are project-level identifiers rather
  than credentials or personal secrets, and no token of any kind has ever been
  committed (verified by full-history scan). Anyone browsing old commits will
  find this note here instead of a silent cover-up.
- **Machine hostnames may appear in historical commit messages** (the project
  signs commits with instance/host provenance as part of its governance
  discipline). These are weak identifiers of no security value.

## Verification

Before each release, the packager runs five gates (root SKILL.md, zero
dot-files/extension-less entries, zero flattened-prefix residue, zero broken
internal links, hook scripts included). Additionally, a private-content needle
scan (home directories, hostnames, tokens, private drive letters, personal
identifiers) is run against the release tree and full git history.

## Reporting

If you believe any file in the current tree or latest release still contains
private or sensitive content, please open an issue instead of a private fork —
we treat privacy leaks as top-priority and will acknowledge within days.
